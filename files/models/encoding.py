import json
import hashlib
import os
import tempfile

from django.conf import settings
from django.core.files import File
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .. import helpers
from .utils import (
    CODECS,
    ENCODE_EXTENSIONS,
    ENCODE_RESOLUTIONS,
    MEDIA_ENCODING_STATUS,
    encoding_media_file_path,
)


class EncodeProfile(models.Model):
    """Encode Profile model
    keeps information for each profile
    """

    name = models.CharField(_("名称"), max_length=90)

    extension = models.CharField(_("扩展名"), max_length=10, choices=ENCODE_EXTENSIONS)

    resolution = models.IntegerField(_("分辨率"), choices=ENCODE_RESOLUTIONS, blank=True, null=True)

    codec = models.CharField(_("编解码器"), max_length=10, choices=CODECS, blank=True, null=True)

    description = models.TextField(_("描述"), blank=True, help_text=_("描述"))

    active = models.BooleanField(_("激活"), default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["resolution"]
        verbose_name = _("编码配置")
        verbose_name_plural = _("编码配置")


class Encoding(models.Model):
    """Encoding Media Instances"""

    add_date = models.DateTimeField(_("添加日期"), auto_now_add=True)

    commands = models.TextField(_("命令"), blank=True, help_text=_("运行的命令"))

    chunk = models.BooleanField(_("分块"), default=False, db_index=True, help_text=_("是否为分块？"))

    chunk_file_path = models.CharField(_("分块文件路径"), max_length=400, blank=True)

    chunks_info = models.TextField(_("分块信息"), blank=True)

    logs = models.TextField(_("日志"), blank=True)

    md5sum = models.CharField(_("MD5校验"), max_length=50, blank=True, null=True)

    media = models.ForeignKey("Media", on_delete=models.CASCADE, related_name="encodings", verbose_name=_("媒体"))

    media_file = models.FileField(_("编码文件"), upload_to=encoding_media_file_path, blank=True, max_length=500)

    profile = models.ForeignKey(EncodeProfile, on_delete=models.CASCADE, verbose_name=_("配置"))

    progress = models.PositiveSmallIntegerField(_("进度"), default=0)

    update_date = models.DateTimeField(_("更新日期"), auto_now=True)

    retries = models.IntegerField(_("重试次数"), default=0)

    size = models.CharField(_("大小"), max_length=20, blank=True)

    status = models.CharField(_("状态"), max_length=20, choices=MEDIA_ENCODING_STATUS, default="pending")

    temp_file = models.CharField(_("临时文件"), max_length=400, blank=True)

    task_id = models.CharField(_("任务ID"), max_length=100, blank=True)

    total_run_time = models.IntegerField(_("总运行时间"), default=0)

    worker = models.CharField(_("工作进程"), max_length=100, blank=True)

    @property
    def media_encoding_url(self):
        if self.media_file:
            return helpers.url_from_path(self.media_file.path)
        return None

    @property
    def media_chunk_url(self):
        if self.chunk_file_path:
            return helpers.url_from_path(self.chunk_file_path)
        return None

    def save(self, *args, **kwargs):
        if self.media_file:
            # Windows 兼容：使用 os.path.getsize 而不是 stat 命令
            try:
                size = os.path.getsize(self.media_file.path)
                self.size = helpers.show_file_size(size)
            except OSError:
                pass
        if self.chunk_file_path and not self.md5sum:
            # Windows 兼容：使用 Python hashlib 而不是 md5sum 命令
            try:
                md5_hash = hashlib.md5()
                with open(self.chunk_file_path, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b''):
                        md5_hash.update(chunk)
                self.md5sum = md5_hash.hexdigest()
            except Exception:
                self.md5sum = ""

        super(Encoding, self).save(*args, **kwargs)

    def update_size_without_save(self):
        """Update the size of an encoding without saving to avoid calling signals"""
        if self.media_file:
            # Windows 兼容：使用 os.path.getsize 而不是 stat 命令
            try:
                size = os.path.getsize(self.media_file.path)
                size = helpers.show_file_size(size)
                Encoding.objects.filter(pk=self.pk).update(size=size)
                return True
            except OSError:
                pass
        return False

    def set_progress(self, progress, commit=True):
        if isinstance(progress, int):
            if 0 <= progress <= 100:
                self.progress = progress
                # save object with filter update
                # to avoid calling signals
                Encoding.objects.filter(pk=self.pk).update(progress=progress)
                return True
        return False

    def __str__(self):
        return f"{self.profile.name}-{self.media.title}"

    class Meta:
        verbose_name = _("编码")
        verbose_name_plural = _("编码")

    def get_absolute_url(self):
        return reverse("api_get_encoding", kwargs={"encoding_id": self.id})


@receiver(post_save, sender=Encoding)
def encoding_file_save(sender, instance, created, **kwargs):
    """Performs actions on encoding file delete
    For example, if encoding is a chunk file, with encoding_status success,
    perform a check if this is the final chunk file of a media, then
    concatenate chunks, create final encoding file and delete chunks
    """

    if instance.chunk and instance.status == "success":
        # a chunk got completed

        # check if all chunks are OK
        # then concatenate to new Encoding - and remove chunks
        # this should run only once!
        if instance.media_file:
            try:
                orig_chunks = json.loads(instance.chunks_info).keys()
            except BaseException:
                instance.delete()
                return False

            chunks = Encoding.objects.filter(
                media=instance.media,
                profile=instance.profile,
                chunks_info=instance.chunks_info,
                chunk=True,
            ).order_by("add_date")

            complete = True

            # perform validation, make sure everything is there
            for chunk in orig_chunks:
                if not chunks.filter(chunk_file_path=chunk):
                    complete = False
                    break

            for chunk in chunks:
                if not (chunk.media_file and chunk.media_file.path):
                    complete = False
                    break

            if complete:
                # concatenate chunks and create final encoding file
                chunks_paths = [f.media_file.path for f in chunks]

                with tempfile.TemporaryDirectory(dir=settings.TEMP_DIRECTORY) as temp_dir:
                    seg_file = helpers.create_temp_file(suffix=".txt", dir=temp_dir)
                    tf = helpers.create_temp_file(suffix=f".{instance.profile.extension}", dir=temp_dir)
                    with open(seg_file, "w") as ff:
                        for f in chunks_paths:
                            ff.write(f"file {f}\n")
                    cmd = [
                        settings.FFMPEG_COMMAND,
                        "-y",
                        "-f",
                        "concat",
                        "-safe",
                        "0",
                        "-i",
                        seg_file,
                        "-c",
                        "copy",
                        "-pix_fmt",
                        "yuv420p",
                        "-movflags",
                        "faststart",
                        tf,
                    ]
                    stdout = helpers.run_command(cmd)

                    encoding = Encoding(
                        media=instance.media,
                        profile=instance.profile,
                        status="success",
                        progress=100,
                    )
                    all_logs = "\n".join([st.logs for st in chunks])
                    encoding.logs = f"{chunks_paths}\n{stdout}\n{all_logs}"
                    workers = list(set([st.worker for st in chunks]))
                    encoding.worker = json.dumps({"workers": workers})

                    start_date = min([st.add_date for st in chunks])
                    end_date = max([st.update_date for st in chunks])
                    encoding.total_run_time = (end_date - start_date).seconds
                    encoding.save()

                    with open(tf, "rb") as f:
                        myfile = File(f)
                        output_name = f"{helpers.get_file_name(instance.media.media_file.path)}.{instance.profile.extension}"
                        encoding.media_file.save(content=myfile, name=output_name)

                    # encoding is saved, deleting chunks
                    # and any other encoding that might exist
                    # first perform one last validation
                    # to avoid that this is run twice
                    if (
                        len(orig_chunks)
                        == Encoding.objects.filter(  # noqa
                            media=instance.media,
                            profile=instance.profile,
                            chunks_info=instance.chunks_info,
                        ).count()
                    ):
                        # if two chunks are finished at the same time, this
                        # will be changed
                        who = Encoding.objects.filter(media=encoding.media, profile=encoding.profile).exclude(id=encoding.id)
                        who.delete()
                    else:
                        encoding.delete()
                    if not Encoding.objects.filter(chunks_info=instance.chunks_info):
                        # TODO: in case of remote workers, files should be deleted
                        # example
                        # for worker in workers:
                        #    for chunk in json.loads(instance.chunks_info).keys():
                        #        remove_media_file.delay(media_file=chunk)
                        for chunk in json.loads(instance.chunks_info).keys():
                            helpers.rm_file(chunk)
                    instance.media.post_encode_actions(encoding=instance, action="add")

    elif instance.chunk and instance.status == "fail":
        encoding = Encoding(media=instance.media, profile=instance.profile, status="fail", progress=100)

        chunks = Encoding.objects.filter(media=instance.media, chunks_info=instance.chunks_info, chunk=True).order_by("add_date")

        chunks_paths = [f.media_file.path for f in chunks]

        all_logs = "\n".join([st.logs for st in chunks])
        encoding.logs = f"{chunks_paths}\n{all_logs}"
        workers = list(set([st.worker for st in chunks]))
        encoding.worker = json.dumps({"workers": workers})
        start_date = min([st.add_date for st in chunks])
        end_date = max([st.update_date for st in chunks])
        encoding.total_run_time = (end_date - start_date).seconds
        encoding.save()

        who = Encoding.objects.filter(media=encoding.media, profile=encoding.profile).exclude(id=encoding.id)

        who.delete()
        # TODO: merge with above if, do not repeat code
    else:
        if instance.status in ["fail", "success"]:
            instance.media.post_encode_actions(encoding=instance, action="add")

        encodings = set([encoding.status for encoding in Encoding.objects.filter(media=instance.media)])
        if ("running" in encodings) or ("pending" in encodings):
            return


@receiver(post_delete, sender=Encoding)
def encoding_file_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Encoding` object is deleted.
    """

    if instance.media_file:
        helpers.rm_file(instance.media_file.path)
        if not instance.chunk:
            instance.media.post_encode_actions(encoding=instance, action="delete")
    # delete local chunks, and remote chunks + media file. Only when the
    # last encoding of a media is complete
