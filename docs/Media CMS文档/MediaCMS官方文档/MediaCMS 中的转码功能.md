# MediaCMS 中的转码功能

MediaCMS 使用 FFmpeg 对媒体文件进行转码。大部分转码设置和配置都在 `files/helpers.py`文件中定义。

## 配置选项

在 `cms/settings.py`中可以自定义多个转码参数：

### FFmpeg 预设

默认的 FFmpeg 预设为 "medium"。此设置控制编码速度和压缩效率之间的权衡。

```
# ffmpeg 选项
FFMPEG_DEFAULT_PRESET = "medium" # 参见 https://trac.ffmpeg.org/wiki/Encode/H.264
```

可用的预设包括：

- ultrafast
- superfast
- veryfast
- faster
- fast
- medium（默认）
- slow
- slower
- veryslow

更快的预设会导致相同质量下文件体积更大，而更慢的预设能提供更好的压缩率但编码时间更长。

### 其他转码设置

`settings.py`中的其他转码设置包括：

- `FFMPEG_COMMAND`：FFmpeg 可执行文件的路径
- `FFPROBE_COMMAND`：FFprobe 可执行文件的路径
- `DO_NOT_TRANSCODE_VIDEO`：如果设置为 True，则只显示原始视频而不进行转码
- `CHUNKIZE_VIDEO_DURATION`：对于超过此时长（以秒为单位）的视频，它们将被分割成块并独立编码
- `VIDEO_CHUNKS_DURATION`：每个视频块的时长（必须小于 CHUNKIZE_VIDEO_DURATION）
- `MINIMUM_RESOLUTIONS_TO_ENCODE`：始终编码这些分辨率，即使需要放大（upscaling）

## 高级配置

如需更高级的转码设置，您可能需要修改 `files/helpers.py`中的以下内容：

- 不同编解码器和分辨率的视频码率
- 音频编码器和码率
- CRF（恒定速率因子）值
- 关键帧设置
- 不同编解码器（H.264、H.265、VP9）的编码参数