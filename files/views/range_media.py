"""
提供支持HTTP Range请求的媒体文件服务
用于解决视频拖动进度条和跳转的问题
"""
import os
import re
from pathlib import Path
from django.http import StreamingHttpResponse, Http404, HttpResponse
from django.conf import settings
from django.views import View


def parse_range_header(range_header, file_size):
    """
    解析HTTP Range头
    返回 (start, end) 元组
    """
    if not range_header:
        return 0, file_size - 1
    
    # Range格式: bytes=start-end
    match = re.match(r'bytes=(\d+)-(\d*)', range_header)
    if not match:
        return 0, file_size - 1
    
    start = int(match.group(1))
    end = match.group(2)
    end = int(end) if end else file_size - 1
    
    # 验证范围
    if start >= file_size:
        return None, None
    if end >= file_size:
        end = file_size - 1
    
    return start, end


class RangeFileIterator:
    """
    文件范围迭代器，用于分块读取文件的指定范围
    """
    def __init__(self, file_path, start=0, end=None, chunk_size=8192):
        self.file_path = file_path
        self.start = start
        self.end = end
        self.chunk_size = chunk_size
        self.file = None
    
    def __iter__(self):
        self.file = open(self.file_path, 'rb')
        self.file.seek(self.start)
        
        remaining = (self.end - self.start + 1) if self.end else None
        
        while True:
            if remaining is not None and remaining <= 0:
                break
            
            chunk_size = self.chunk_size
            if remaining is not None and remaining < chunk_size:
                chunk_size = remaining
            
            chunk = self.file.read(chunk_size)
            if not chunk:
                break
            
            if remaining is not None:
                remaining -= len(chunk)
            
            yield chunk
        
        if self.file:
            self.file.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        if self.file:
            self.file.close()


class ServeMediaWithRange(View):
    """
    提供支持HTTP Range请求的媒体文件服务
    """
    
    def get(self, request, path):
        """
        处理GET请求，支持Range请求
        """
        # 构建完整的文件路径
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        file_path = os.path.normpath(file_path)
        
        # 安全检查：确保路径在MEDIA_ROOT内
        if not file_path.startswith(os.path.normpath(settings.MEDIA_ROOT)):
            raise Http404("Invalid path")
        
        # 检查文件是否存在
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise Http404("File not found")
        
        # 获取文件信息
        file_size = os.path.getsize(file_path)
        
        # 获取Range请求头
        range_header = request.META.get('HTTP_RANGE', '')
        
        # 确定内容类型
        content_type = self.get_content_type(file_path)
        
        # 如果没有Range请求，返回完整文件
        if not range_header:
            response = StreamingHttpResponse(
                RangeFileIterator(file_path, 0, file_size - 1),
                content_type=content_type
            )
            response['Content-Length'] = str(file_size)
            response['Accept-Ranges'] = 'bytes'
            return response
        
        # 解析Range头
        start, end = parse_range_header(range_header, file_size)
        
        if start is None:
            # 无效的Range请求
            response = HttpResponse(status=416)  # Range Not Satisfiable
            response['Content-Range'] = f'bytes */{file_size}'
            return response
        
        # 返回部分内容
        content_length = end - start + 1
        response = StreamingHttpResponse(
            RangeFileIterator(file_path, start, end),
            status=206,  # Partial Content
            content_type=content_type
        )
        response['Content-Length'] = str(content_length)
        response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
        response['Accept-Ranges'] = 'bytes'
        
        return response
    
    def get_content_type(self, file_path):
        """
        根据文件扩展名确定Content-Type
        """
        import mimetypes
        
        content_type, _ = mimetypes.guess_type(file_path)
        
        if not content_type:
            # 默认类型
            ext = Path(file_path).suffix.lower()
            content_types = {
                '.mp4': 'video/mp4',
                '.webm': 'video/webm',
                '.ogg': 'video/ogg',
                '.m3u8': 'application/vnd.apple.mpegurl',
                '.ts': 'video/mp2t',
                '.mp3': 'audio/mpeg',
                '.wav': 'audio/wav',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
            }
            content_type = content_types.get(ext, 'application/octet-stream')
        
        return content_type

