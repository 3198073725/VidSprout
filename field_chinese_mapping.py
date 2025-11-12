#!/usr/bin/env python
"""
字段中文化映射表
"""

# 常用字段的中文翻译映射
FIELD_TRANSLATIONS = {
    # 基础字段
    'title': '标题',
    'description': '描述',
    'name': '名称',
    'slug': '网址别名',
    'add_date': '添加日期',
    'edit_date': '编辑日期',
    'created_at': '创建时间',
    'updated_at': '更新时间',
    'user': '用户',
    'author': '作者',
    'owner': '所有者',
    
    # 媒体相关字段
    'media': '媒体',
    'media_file': '媒体文件',
    'thumbnail': '缩略图',
    'poster': '海报',
    'duration': '时长',
    'size': '大小',
    'views': '观看次数',
    'likes': '点赞数',
    'dislikes': '不喜欢数',
    'comments_count': '评论数',
    'rating': '评分',
    
    # 状态字段
    'status': '状态',
    'state': '状态',
    'is_active': '是否激活',
    'is_public': '是否公开',
    'is_featured': '是否推荐',
    'is_reviewed': '是否已审核',
    'published': '是否发布',
    'enabled': '是否启用',
    
    # 编码相关
    'encoding_status': '编码状态',
    'profile': '编码配置',
    'resolution': '分辨率',
    'codec': '编解码器',
    'bitrate': '比特率',
    'framerate': '帧率',
    
    # 分类和标签
    'category': '分类',
    'categories': '分类',
    'tag': '标签',
    'tags': '标签',
    
    # 评论相关
    'comment': '评论',
    'text': '内容',
    'parent': '父评论',
    
    # 用户相关
    'username': '用户名',
    'email': '邮箱',
    'first_name': '名',
    'last_name': '姓',
    'full_name': '全名',
    'password': '密码',
    
    # 文件相关
    'file': '文件',
    'path': '路径',
    'url': '链接',
    'extension': '扩展名',
    'mime_type': 'MIME类型',
    
    # 其他常用字段
    'language': '语言',
    'subtitle': '字幕',
    'license': '许可证',
    'copyright': '版权',
    'privacy': '隐私设置',
    'permissions': '权限',
}

# 帮助文本的中文翻译
HELP_TEXT_TRANSLATIONS = {
    'Whether comments will be allowed for this media': '是否允许对此媒体进行评论',
    'Whether media is globally featured by a MediaCMS editor': '媒体是否被MediaCMS编辑全局推荐',
    'Identifier for the Media': '媒体的标识符',
    'Path to HLS file for videos': '视频HLS文件的路径',
    'Media can exist in one or no Channels': '媒体可以存在于一个或零个频道中',
    'File has to be WebVTT format': '文件必须是WebVTT格式',
    'Thumbnail to show on listings': '在列表中显示的缩略图',
    'global categories or user specific': '全局分类或用户特定分类',
    'number of media': '媒体数量',
    'commands run': '运行的命令',
    'is chunk?': '是否为分块？',
    'language code': '语言代码',
    'Chapter data': '章节数据',
    'Timestamps for trimming': '剪切时间戳',
}

def get_chinese_field_name(field_name):
    """获取字段的中文名称"""
    return FIELD_TRANSLATIONS.get(field_name, field_name)

def get_chinese_help_text(help_text):
    """获取帮助文本的中文翻译"""
    return HELP_TEXT_TRANSLATIONS.get(help_text, help_text)

if __name__ == '__main__':
    print("字段中文化映射表")
    print("=" * 50)
    for en, cn in FIELD_TRANSLATIONS.items():
        print(f"{en:20} -> {cn}")
