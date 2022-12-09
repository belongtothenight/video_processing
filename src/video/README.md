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
EX: python compress_video.py %userprofile%\Videos\Minecraft\mp4_files_YT_test1.txt
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

### Installation

1. windows
    1. Download "ffmpeg" via <https://ffmpeg.org/download.html>, and add ffmpeg to system variable.
    2. Type "ffmpeg" in cmd to check whether it's setup correctly.
    3. Download Python.
    4. Type "pip install send2trash" to install required library.
    5. Create a list of video files in txt format like the example below.
    6. Use the above mentioned "execute command" to start executing.
2. linux
    1. Use terminal to install ffmpeg
    2. Use terminal to install python
    3. Use terminal to install python library "send2trash"
    4. Create a list of video files in txt format like the example below.
    5. Use the above mentioned "execute command" to start executing.

list of video files example (txt):

```
D:/1.mp4
D:/2.mp4
D:/3.mp4
```

### possible improvement

Add a central file database to keep record of processed files.

## <a name="2"></a>list_file.py

### requirement

python

### execute command

python list_file.py

### possible improvement

Add an option of file create/modify date, and list out all files after(before?) that.
