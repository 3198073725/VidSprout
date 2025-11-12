from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from .. import helpers
from .utils import category_thumb_path, generate_uid


class Category(models.Model):
    """A Category base model"""

    uid = models.CharField(_("唯一标识"), unique=True, max_length=36, default=generate_uid)

    add_date = models.DateTimeField(_("添加日期"), auto_now_add=True)

    title = models.CharField(_("标题"), max_length=100, db_index=True)

    description = models.TextField(_("描述"), blank=True)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("用户"))

    is_global = models.BooleanField(_("全局分类"), default=False, help_text=_("全局分类或用户特定分类"))

    media_count = models.IntegerField(_("媒体数量"), default=0, help_text=_("媒体数量"))

    thumbnail = ProcessedImageField(
        upload_to=category_thumb_path,
        processors=[ResizeToFit(width=344, height=None)],
        format="JPEG",
        options={"quality": 85},
        blank=True,
        verbose_name=_("缩略图"),
    )

    listings_thumbnail = models.CharField(_("列表缩略图"), max_length=400, blank=True, null=True, help_text=_("在列表中显示的缩略图"))

    is_rbac_category = models.BooleanField(_("基于角色的访问控制"), default=False, db_index=True, help_text=_('分类访问是否由用户组角色控制'))

    identity_provider = models.ForeignKey(
        'socialaccount.SocialApp',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='categories',
        help_text=_('分类是否与特定身份提供商相关'),
        verbose_name=_('身份提供商配置'),
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
        verbose_name = _("分类")
        verbose_name_plural = _("分类")

    def get_absolute_url(self):
        return f"{reverse('search')}?c={self.title}"

    def update_category_media(self):
        """Set media_count"""

        # Always set number of Category the total number of media
        # Depending on how RBAC is set and Permissions etc it is
        # possible that users won't see all media in a Category
        # but it's worth to handle this on the UI level
        # (eg through a message that says that you see only files you have permissions to see)

        self.media_count = Media.objects.filter(category=self).count()
        self.save(update_fields=["media_count"])

        # OLD logic
        # if getattr(settings, 'USE_RBAC', False) and self.is_rbac_category:
        #    self.media_count = Media.objects.filter(category=self).count()
        # else:
        #    self.media_count = Media.objects.filter(listable=True, category=self).count()

        self.save(update_fields=["media_count"])
        return True

    @property
    def thumbnail_url(self):
        """Return thumbnail for category
        prioritize processed value of listings_thumbnail
        then thumbnail
        """

        if self.thumbnail:
            return helpers.url_from_path(self.thumbnail.path)

        if self.listings_thumbnail:
            return self.listings_thumbnail

        if Media.objects.filter(category=self, state="public").exists():
            media = Media.objects.filter(category=self, state="public").order_by("-views").first()
            if media:
                return media.thumbnail_url

        return None

    def save(self, *args, **kwargs):
        strip_text_items = ["title", "description"]
        for item in strip_text_items:
            setattr(self, item, strip_tags(getattr(self, item, None)))
        super(Category, self).save(*args, **kwargs)


class Tag(models.Model):
    """A Tag model"""

    title = models.CharField(_("标题"), max_length=100, unique=True, db_index=True)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("用户"))

    media_count = models.IntegerField(_("媒体数量"), default=0, help_text=_("媒体数量"))

    listings_thumbnail = models.CharField(
        _("列表缩略图"),
        max_length=400,
        blank=True,
        null=True,
        help_text=_("在列表中显示的缩略图"),
        db_index=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
        verbose_name = _("标签")
        verbose_name_plural = _("标签")

    def get_absolute_url(self):
        return f"{reverse('search')}?t={self.title}"

    def update_tag_media(self):
        self.media_count = Media.objects.filter(state="public", is_reviewed=True, tags=self).count()
        self.save(update_fields=["media_count"])
        return True

    def save(self, *args, **kwargs):
        self.title = helpers.get_alphanumeric_only(self.title)
        self.title = self.title[:100]
        super(Tag, self).save(*args, **kwargs)

    @property
    def thumbnail_url(self):
        if self.listings_thumbnail:
            return self.listings_thumbnail
        media = Media.objects.filter(tags=self, state="public").order_by("-views").first()
        if media:
            return media.thumbnail_url

        return None


# Import Media to avoid circular imports
from .media import Media  # noqa
