import sys
import subprocess
import os
from pathlib import Path
from time import sleep
from datetime import datetime
os.system('cls')

'''
Requirements:
Windows: ffmpeg, cmdutils
Linux: ffmpeg
'''


def time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y:%H:%M:%S")


class compress_video():
    def __init__(self, show=False):
        if len(sys.argv) < 2:
            print('Please provide a file name.')
            sys.exit()
        # sys.argv[1] is the path and name to the video file log
        # sys.argv[?] is whether to update file log or not ("-remove_log" to remove)
        # sys.argv[?] windows or linux ("-windows" or "-linux")
        # sys.argv[?] delete or recycle old video ("-del" or "-recycle")
        self.file_name = sys.argv[0]
        self.file_path = sys.argv[1]
        self.record_path = os.path.dirname(self.file_path) + "\\record.txt"
        self.log_remove = False
        self.shell = False
        self.del_old = False
        if '-remove_log' in sys.argv:
            self.log_remove = True
        if '-windows' in sys.argv:
            self.shell = False
        elif '-linux' in sys.argv:
            self.shell = True
        if '-del' in sys.argv:
            self.del_old = True
        if show:
            print('file_name: ' + self.file_name)
            print('file_path: ' + self.file_path)
            print('record_path: ' + self.record_path)
            print('log_remove: ' + str(self.log_remove))
            print('shell: ' + str(self.shell))
            print('del_old: ' + str(self.del_old))

    def read_log(self):
        # get the log file contents
        with open(self.file_path, 'r') as f:
            self.lines = f.readlines()

    def remove_identical_lines(self):
        # remove identical lines
        pass

    def compress(self):
        self.progress = 0
        self.total = len(self.lines)
        while True:
            self.progress += 1
            try:
                self.video_path = self.lines[0]
            except IndexError:
                print('{0} >> {1} >> No more videos to compress'.format(
                    self.file_name, time()))
                break
            self.video_path = self.video_path.replace('\n', '')
            self.nvideo_path = self.video_path.replace(
                '.mp4', '_temp.mp4')
            self.video_path = str(Path(self.video_path))
            self.nvideo_path = str(Path(self.nvideo_path))
            print('{0} >> {1} >> progress: {2}/{3} {4}%'.format(
                self.file_name, time(), self.progress, self.total, format(self.progress/self.total*100, '.2f')))
            print('{0} >> {1} >> video_path: {2}'.format(
                self.file_name, time(), self.video_path))
            print('{0} >> {1} >> temp_path: {2}'.format(
                self.file_name, time(), self.nvideo_path))

            # check file exists
            exist = os.path.isfile(self.video_path)
            if not exist:
                l = '{0} >> {1} >> {2} doesn\'t exist'.format(
                    self.file_name, time(), self.video_path)
                print(l)
                with open(self.record_path, 'a') as f:
                    f.write(l + '\n')
                self.lines.pop(0)
                continue
            print('{0} >> {1} >> processing {2}'.format(
                self.file_name, time(), os.path.basename(self.video_path)))

            # get video size pre-compression
            ffprobe_cmd = 'ffprobe -v error -show_entries format=size -of default=nokey=1:noprint_wrappers=1 "{0}"'.format(
                self.video_path)
            self.prepsize = int((subprocess.check_output(
                ffprobe_cmd, shell=self.shell)).decode('utf-8'))

            # compressing video
            ffmpeg_cmd = 'ffmpeg -v quiet -stats -y -i "{0}" -vcodec h264 -acodec aac "{1}"'.format(
                self.video_path, self.nvideo_path)
            # https://stackoverflow.com/questions/4951099/getting-progress-message-from-a-subprocess
            p = subprocess.Popen(
                ffmpeg_cmd, shell=self.shell, stdout=subprocess.PIPE)
            while True:
                cmd_line = p.stdout.readline()
                if not cmd_line:
                    break
                print(cmd_line.decode('utf-8'))
            print('{0} >> {1} >> compressed {2}'.format(
                self.file_name, time(), os.path.basename(self.nvideo_path)))

            # recycle the old video
            if self.shell:
                if self.del_old:
                    recycle_cmd = 'rm "{0}"'.format(self.video_path)
                else:
                    recycle_cmd = 'gio trash "{0}"'.format(self.video_path)
            else:
                if self.del_old:
                    recycle_cmd = 'del "{0}"'.format(self.video_path)
                else:
                    recycle_cmd = 'recycle "{0}"'.format(self.video_path)
            subprocess.call(recycle_cmd, shell=self.shell)
            if self.del_old:
                print('{0} >> {1} >> deleted {2}'.format(
                    self.file_name, time(), os.path.basename(self.video_path)))
            else:
                print('{0} >> {1} >> recycled {2}'.format(
                    self.file_name, time(), os.path.basename(self.video_path)))

            # rename the new video
            os.rename(self.nvideo_path, self.video_path)
            print('{0} >> {1} >> renamed {2}'.format(
                self.file_name, time(), os.path.basename(self.nvideo_path)))

            # get video size post-compression
            ffprobe_cmd = 'ffprobe -v error -show_entries format=size -of default=nokey=1:noprint_wrappers=1 "{0}"'.format(
                self.video_path)
            self.postpsize = int((subprocess.check_output(
                ffprobe_cmd, shell=self.shell)).decode('utf-8'))

            # calculate compression ratio / size reduction
            l = '{0} >> {1} >> ratio: {2}% >> saved {3}MB >> compressed {4}'.format(
                self.file_name, time(), format(self.postpsize/self.prepsize*100, '.4f'), format((self.prepsize-self.postpsize)/(2**23), '10.2f'), os.path.basename(self.video_path))
            print(l)
            with open(self.record_path, 'a') as f:
                f.write(l + '\n')
            # remove the line from the log file
            try:
                self.lines.remove(self.video_path + '\n')
            except ValueError:
                self.lines.remove(self.video_path)
            if self.log_remove:
                with open(self.file_path, 'w') as f:
                    f.writelines(self.lines)
            if self.progress >= self.total:
                break
            print()

        # end
        print('\n{0} >> {1} >> finished compressing all designated files.'.format(
            self.file_name, time()))


# main
if __name__ == '__main__':
    cv = compress_video()
    cv.read_log()
    cv.remove_identical_lines()
    cv.compress()
