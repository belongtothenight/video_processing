# SRC

This is the detail of each python files.

## AnchorLink

1. [compress_video.py](#1)
2. [list_file.py](#2)

## <a name="1"></a>compress_video.py

Only tested with mp4 videos for now.

### requirement

1. windows: python, python-send2trash, ffmpeg
2. linux: python, python-send2trash, ffmpeg

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

### possible features

1. hide all files path info
2. add ETA
3. restructure code

## <a name="2"></a>list_file.py

### requirement

python

### execute command

python list_file.py
