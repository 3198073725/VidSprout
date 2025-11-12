# Windows FFmpeg 安装和配置指南

## 🔍 问题分析

错误信息：`FileNotFoundError: [WinError 2] 系统找不到指定的文件`

**原因：**
1. FFmpeg/FFprobe 未安装或未添加到系统 PATH
2. MediaCMS 代码中使用了 Unix 命令（`stat`、`md5sum`），在 Windows 上不可用

---

## ✅ 解决方案

### 步骤 1：安装 FFmpeg

#### 方法 A：使用 Chocolatey（推荐）

```powershell
# 以管理员身份运行 PowerShell
choco install ffmpeg
```

#### 方法 B：手动安装

1. **下载 FFmpeg**
   - 访问：https://www.gyan.dev/ffmpeg/builds/
   - 下载 `ffmpeg-release-essentials.zip`
   - 或使用：https://github.com/BtbN/FFmpeg-Builds/releases

2. **解压到目录**
   ```
   例如：C:\ffmpeg
   ```

3. **添加到 PATH**
   - 右键"此电脑" → "属性" → "高级系统设置"
   - 点击"环境变量"
   - 在"系统变量"中找到 `Path`，点击"编辑"
   - 点击"新建"，添加 FFmpeg 的 `bin` 目录路径（例如：`C:\ffmpeg\bin`）
   - 点击"确定"保存

4. **验证安装**
   ```powershell
   ffmpeg -version
   ffprobe -version
   ```

---

### 步骤 2：修复 Windows 兼容性问题

MediaCMS 的 `files/helpers.py` 使用了 Unix 命令，需要修改为 Windows 兼容代码。

**需要修改的函数：**
- `media_file_info()` - 使用 `stat` 和 `md5sum`

**修复方案：**
使用 Python 内置函数替代 Unix 命令：
- `os.path.getsize()` 替代 `stat`
- `hashlib.md5()` 替代 `md5sum`

---

## 🔧 临时解决方案（开发环境）

### 禁用视频转码（快速测试）

在 `cms/local_settings.py` 中添加：

```python
# 禁用视频转码（开发环境，仅用于测试）
DO_NOT_TRANSCODE_VIDEO = True
```

**注意：** 这会禁用视频转码功能，上传的视频将不会进行编码处理。

---

## 📝 完整修复步骤

### 1. 安装 FFmpeg

按照上述步骤安装 FFmpeg 并添加到 PATH。

### 2. 修改 `files/helpers.py`（Windows 兼容）

找到 `media_file_info()` 函数（约第 235 行），修改以下部分：

**原始代码（Unix）：**
```python
cmd = ["stat", "-c", "%s", input_file]
stdout = run_command(cmd).get("out")
if stdout:
    file_size = int(stdout.strip())
else:
    ret["fail"] = True
    return ret

cmd = ["md5sum", input_file]
stdout = run_command(cmd).get("out")
if stdout:
    md5sum = stdout.split()[0]
else:
    md5sum = ""
```

**修改为（Windows 兼容）：**
```python
# 使用 Python 内置函数替代 Unix 命令
import hashlib

try:
    file_size = os.path.getsize(input_file)
except OSError:
    ret["fail"] = True
    return ret

# 计算 MD5
try:
    with open(input_file, 'rb') as f:
        md5_hash = hashlib.md5()
        for chunk in iter(lambda: f.read(4096), b''):
            md5_hash.update(chunk)
        md5sum = md5_hash.hexdigest()
except Exception:
    md5sum = ""
```

### 3. 验证配置

```bash
# 在 Django shell 中测试
python manage.py shell
>>> from django.conf import settings
>>> import subprocess
>>> subprocess.run([settings.FFMPEG_COMMAND, '-version'])
>>> subprocess.run([settings.FFPROBE_COMMAND, '-version'])
```

---

## ⚠️ 注意事项

1. **PATH 配置**：修改 PATH 后需要重启命令行/Django 服务器才能生效
2. **权限问题**：确保 FFmpeg 可执行文件有执行权限
3. **路径问题**：如果 FFmpeg 不在 PATH 中，可以在 `local_settings.py` 中指定完整路径：
   ```python
   FFMPEG_COMMAND = "C:\\ffmpeg\\bin\\ffmpeg.exe"
   FFPROBE_COMMAND = "C:\\ffmpeg\\bin\\ffprobe.exe"
   ```

---

## 🎯 快速验证

安装 FFmpeg 后，运行以下命令验证：

```powershell
ffmpeg -version
ffprobe -version
```

如果显示版本信息，说明安装成功。

---

## 📚 参考资源

- FFmpeg 官方文档：https://ffmpeg.org/documentation.html
- Windows 安装指南：https://www.wikihow.com/Install-FFmpeg-on-Windows
- Chocolatey 包管理器：https://chocolatey.org/

