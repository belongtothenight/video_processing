# src/VIDEO

This is the detail of each python files.

## AnchorLink

1. [compress_video.py](#1)
2. [list_file.py](#2)
3. [scale_video.py](#3)

## <a name="1"></a>compress_video.py

<details open>
<summary>Batch re-encode video files to reduce their size.</summary>

### requirement

1. Windows: python, python-send2trash, ffmpeg
2. Linux: python, python-send2trash, ffmpeg

### execute command

1. Windows Command: python "full path of this file" "full path of file list file"<br>
EX: python compress_video.py %userprofile%\Videos\test_files.txt
2. Linux Command: python "full path of this file" "full path of file list file" -linux<br>
EX: python compress_video.py /home/cdc/Desktop/test_files.txt -linux

### command parameter

|    param    |       default        | description                                            |
| :---------: | :------------------: | ------------------------------------------------------ |
|   -linux    |       windows        | operation system                                       |
| -remove_log |    doesn't remove    | remove video path from txt after compressing the video |
|    -del     |       recycle        | delete(permanent) or recycle(temporary) old video      |
|     -h0     |     display all      | hidden file info + length + ETA + Uptime               |
|     -h1     |     display all      | hidden file info                                       |
|     -ac     | doesn't clear screen | auto clear screen                                      |

### Installation

If it's your first time using this, copy some of your video files to test them out with different params.

1. windows
    1. Download "ffmpeg" via <https://ffmpeg.org/download.html>, and add ffmpeg to system variable.
    2. Type "ffmpeg" in cmd to check whether it's setup correctly.
    3. Download Python.
    4. Type "pip install send2trash" to install required library.
    5. Create a list of video files in txt format like the example below.
    6. Use the above mentioned "execute command" in cmd to start executing.
2. linux
    1. Use terminal to install ffmpeg
    2. Use terminal to install python
    3. Use terminal to install python library "send2trash"
    4. Create a list of video files in txt format like the example below.
    5. Use the above mentioned "execute command" in terminal to start executing.

list of video files example (test.txt):

```
D:/1.mp4
D:/2.mp4
D:/3.mp4
```

execute command: python compress_video.py test.txt

### possible improvement

1. Add a central file database to keep record of processed files.
2. Rework on arguments.

</details>

## <a name="2"></a>list_file.py

<details open>
<summary>Export a txt file containing file path of files with the specified format.</summary>

### requirement

python

### execution

Execute with: "python list_file.py"

After execution, answer the questions:

| Question                                       | Sample input     |
| ---------------------------------------------- | ---------------- |
| Enter the path to the root of exporting files: | D:/              |
| Enter the path to export file log:             | D:/mp4_files.txt |
| Enter the format of files to export:           | mp4              |

Sample file structure:<br>
D:<br>
|-1.mp4<br>
|-videos<br>
&nbsp;&nbsp;&nbsp;&nbsp;|-2.mp4<br>

Sample export txt (mp4_files.txt) content:

```
D:/1.mp4
D:/videos/2.mp4
```

</details>

## <a name="3"></a>scale_video.py

<details open>
<summary>Scale up or down videos in batch.</summary>

### execute command

1. Windows Command: python "full path of this file" "full path of file list file" "scale" "algorithm"<br>
EX: python scale_video.py %userprofile%\Videos\test_files.txt 2560x1440 lanczos
1. Linux Command: python "full path of this file" "full path of file list file" "scale" "algorithm" -linux<br>
EX: python compress_video.py /home/cdc/Desktop/test_files.txt 2560x1440 lanczos -linux

### command parameter

|    param    | default | description                                            |
| :---------: | :-----: | ------------------------------------------------------ |
| sys.argv[1] |    ~    | file log path                                          |
| sys.argv[2] |    ~    | scale size                                             |
| sys.argv[3] |    ~    | algorithm (bilinear/bicubic/lanczos)                   |
|   --help    |    ~    | print help info                                        |
|   --linux   | windows | operation system                                       |
|   --hd 0    |    ~    | hidden file info + length + ETA + Uptime               |
|   --hd 1    |    ~    | hidden file info                                       |
|    --cs     |    ~    | clear screen                                           |
|    --icf    |    ~    | input confirmation                                     |
|    --kl     |    ~    | keep video path from txt after compressing the video |
|    --rov    | delete  | recycle(temporary) old video                           |


### possible improvement

1. Change records lines.

</details>

## FFmpeg NVIDIA GPU Acceleration installation (currently not working with this script.)

<https://docs.nvidia.com/video-technologies/video-codec-sdk/ffmpeg-with-nvidia-gpu/>

## Major Possible Improvement

1. ADD GPU compute option
2. Change scripts to be a standard library with specified arguments to do different tasks.
