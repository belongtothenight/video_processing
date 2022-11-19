# SRC

This is the detail of each python files.

## AnchorLink

1. [compress_video.py](#1)

## <a name="1"></a>compress_video.py

### execute command

1. Windows Commend: python "full path of this file" "full path of file list file"
EX: python compress_video.py C:\Users\dachu\Videos\Minecraft\mp4_files_YT_test1.txt
2. Linux Commend: python "full path of this file" "full path of file list file" -linux
EX: python compress_video.py /home/cdc/Desktop/test_files.txt -linux

### command parameter

| param             | description                                            |
| ----------------- | ------------------------------------------------------ |
| -windows / -linux | operation system                                       |
| -remove_log       | remove video path from txt after compressing the video |
| -del / -recycle   | delete or recycle old video                            |