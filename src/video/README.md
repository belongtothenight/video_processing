# src/VIDEO

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

|    param    |       default        | description                                            |
| :---------: | :------------------: | ------------------------------------------------------ |
|   -linux    |       windows        | operation system                                       |
| -remove_log |    doesn't remove    | remove video path from txt after compressing the video |
|    -del     |       recycle        | delete or recycle old video                            |
|     -h0     |     display all      | hidden file info + length + ETA + Uptime               |
|     -h1     |     display all      | hidden file info                                       |
|     -ac     | doesn't clear screen | auto clear screen                                      |

### Improvement

Add a central file database to keep record of processed files.

## <a name="2"></a>list_file.py

### requirement

python

### execute command

python list_file.py

### Improvement

Add an option of file create/modify date, and list out all files after(before?) that.
