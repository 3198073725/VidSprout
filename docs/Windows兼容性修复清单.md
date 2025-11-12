# MediaCMS Windows 兼容性修复清单

## ✅ 已修复的问题

### 1. 路径处理问题

#### 问题 1：`get_file_name()` 使用 `split("/")`
- **文件**：`files/helpers.py`
- **修复**：使用 `os.path.basename()` 替代 `split("/")`
- **影响**：文件名提取在 Windows 上能正确工作

#### 问题 2：`files/models/media.py` 中使用 `split("/")`
- **文件**：`files/models/media.py` 第243行
- **修复**：使用 `helpers.get_file_name()` 替代 `split("/")`

#### 问题 3：`files/tasks.py` 中使用 `split("/")`
- **文件**：`files/tasks.py` 第140行
- **修复**：使用 `helpers.get_file_name()` 替代 `split("/")`

#### 问题 4：路径拼接使用字符串拼接
- **文件**：`files/tasks.py` 第501、544-545行
- **修复**：使用 `os.path.join()` 替代字符串拼接
- **示例**：
  ```python
  # 修复前
  output_name = f"{tmpdirname}/{subtitle_name}"
  
  # 修复后
  output_name = os.path.join(tmpdirname, subtitle_name)
  ```

#### 问题 5：`glob.glob()` 使用字符串拼接
- **文件**：`files/models/media.py` 第1046行
- **修复**：使用 `os.path.join()` 构建 glob 模式

### 2. Unix 命令问题

#### 问题 1：`stat` 和 `md5sum` 命令
- **文件**：`files/helpers.py` `media_file_info()` 函数
- **修复**：
  - `stat` → `os.path.getsize()`
  - `md5sum` → `hashlib.md5()`

#### 问题 2：`cp` 命令
- **文件**：`files/models/subtitle.py` 第68行
- **修复**：使用 `shutil.copy()` 替代 `cp` 命令

#### 问题 3：`ps aux|grep` 和 `kill` 命令
- **文件**：`files/methods.py` `kill_ffmpeg_process()` 函数
- **修复**：添加 Windows 兼容代码，使用 `wmic` 和 `taskkill` 命令

### 3. 硬编码路径问题

#### 问题 1：Whisper 转录硬编码 Unix 路径
- **文件**：`files/tasks.py` 第503行
- **修复**：使用 `media.media_file.path` 替代硬编码路径
- **修复前**：
  ```python
  cmd = f"whisper /home/mediacms.io/mediacms/media_files/{media.media_file.name} ..."
  ```
- **修复后**：
  ```python
  media_file_path = media.media_file.path
  cmd = f"whisper {media_file_path} ..."
  ```

### 4. 临时目录问题

#### 问题 1：`TEMP_DIRECTORY` 配置为 `/tmp`
- **文件**：`cms/local_settings.py`
- **修复**：使用 `tempfile.gettempdir()` 获取系统临时目录
- **配置**：
  ```python
  TEMP_DIRECTORY = tempfile.gettempdir()  # Windows: C:\Users\...\AppData\Local\Temp
  ```

### 5. URL 路径生成问题

#### 问题 1：`url_from_path()` 路径替换
- **文件**：`files/helpers.py` `url_from_path()` 函数
- **修复**：规范化路径分隔符，确保 Windows 路径正确转换为 URL

## ⚠️ 仍需注意的问题

### 1. ImageMagick `convert` 命令
- **文件**：`files/tasks.py` 第553行
- **说明**：`produce_sprite_from_video()` 函数使用 `convert` 命令（ImageMagick）
- **Windows 要求**：需要安装 ImageMagick 并添加到 PATH
- **替代方案**：如果不需要 sprite 功能，可以跳过

### 2. Whisper 转录功能
- **文件**：`files/tasks.py` `whisper_transcribe()` 函数
- **说明**：需要安装 Whisper Python 包
- **Windows 要求**：需要安装 Whisper 和相关依赖

### 3. PySubs2 字幕转换
- **文件**：`files/models/subtitle.py`
- **说明**：需要安装 `pysubs2` Python 包
- **Windows 要求**：通常可以正常工作

## 📋 Windows 兼容性检查清单

### 必需组件
- ✅ Python 3.11+ 或 3.13
- ✅ PostgreSQL 15+
- ✅ Redis（Memurai 或 WSL）
- ✅ FFmpeg（已安装并添加到 PATH）
- ✅ Django 5.2.6
- ✅ 所有 Python 依赖（requirements-windows.txt）

### 可选组件（用于特定功能）
- ⚠️ ImageMagick（用于 sprite 生成）
- ⚠️ Whisper（用于视频转录）
- ⚠️ PySubs2（用于字幕转换）

### 配置检查
- ✅ `TEMP_DIRECTORY` 配置正确
- ✅ `FFMPEG_COMMAND` 和 `FFPROBE_COMMAND` 配置正确
- ✅ `MEDIA_ROOT` 和 `STATIC_ROOT` 路径正确
- ✅ `CSRF_TRUSTED_ORIGINS` 包含前端地址
- ✅ `CORS_ALLOWED_ORIGINS` 包含前端地址
- ✅ `USERS_CAN_SELF_REGISTER = True`

## 🧪 测试建议

1. **基础功能测试**
   - ✅ 用户注册
   - ✅ 用户登录
   - ✅ 登录状态保持（刷新页面）

2. **媒体上传测试**
   - ✅ 图片上传
   - ✅ 视频上传
   - ✅ 缩略图生成
   - ✅ 视频信息提取

3. **路径处理测试**
   - ✅ 文件路径包含空格和特殊字符
   - ✅ 文件路径包含中文字符
   - ✅ 相对路径和绝对路径处理

4. **临时文件测试**
   - ✅ 临时文件创建
   - ✅ 临时文件清理

## 📝 已修复的文件列表

1. ✅ `files/helpers.py` - 路径处理、Unix 命令替代
2. ✅ `files/models/media.py` - 路径处理、glob 模式
3. ✅ `files/tasks.py` - 路径拼接、硬编码路径
4. ✅ `files/models/subtitle.py` - Unix 命令替代
5. ✅ `files/methods.py` - 进程管理（Windows 兼容）
6. ✅ `cms/local_settings.py` - 临时目录配置

## 🎯 总结

所有主要的 Windows 兼容性问题都已修复：
- ✅ 路径处理使用 `os.path.join()` 和 `os.path.basename()`
- ✅ Unix 命令替换为 Python 内置函数或跨平台库
- ✅ 临时目录配置为 Windows 兼容
- ✅ 硬编码路径已移除
- ✅ 进程管理添加了 Windows 支持

项目现在应该可以在 Windows 上完美运行！🎉

