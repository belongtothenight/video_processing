# SRC

This is the detail of each python files.

## AnchorLink

1. [compress_video.py](#1)

## <a name="1"></a>compress_video.py

Only tested with mp4 videos for now.

### requirement

1. windows: ffmpeg, cmdutils
2. linux: ffmpeg

### execute command

1. Windows Commend: python "full path of this file" "full path of file list file"<br>
EX: python compress_video.py C:\Users\dachu\Videos\Minecraft\mp4_files_YT_test1.txt
2. Linux Commend: python "full path of this file" "full path of file list file" -linux<br>
EX: python compress_video.py /home/cdc/Desktop/test_files.txt -linux

### command parameter

| param             | description                                            |
| ----------------- | ------------------------------------------------------ |
| -windows / -linux | operation system                                       |
| -remove_log       | remove video path from txt after compressing the video |
| -del / -recycle   | delete or recycle old video                            |
