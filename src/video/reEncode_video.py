import sys
import getopt
import subprocess
import os
import time
import timeit
import datetime
from pathlib import Path
from datetime import datetime
from send2trash import send2trash


def currenttime():
    now = datetime.now()
    return now.strftime("%Y/%m/%d:%H:%M:%S")


def s2strdhms(s):
    d, s = divmod(s, 86400)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    d = int(d)
    h = int(h)
    m = int(m)
    s = int(s)
    if s < 10:
        s = "0" + str(s)
    if m < 10:
        m = "0" + str(m)
    if h < 10:
        h = "0" + str(h)
    tstring = '{0}:{1}:{2}:{3}'.format(d, h, m, s)
    return tstring


class compress_video():
    def __init__(self, show=False):
        '''
        sys.argv[1] path and name to the video file log
        sys.argv[?] (--nrmfl)  not remove file list of processed files
        sys.argv[?] (--linux)  linux os
        sys.argv[?] (--rc)     recycle old video
        sys.argv[?] (--hd 0)   hidden file info + length + ETA
        sys.argv[?] (--hd 1)   hidden file info
        sys.argv[?] (--nacs)   not auto clear screen
        sys.argv[?] (--gpu)    use gpu
        sys.argv[?] (--sp)     show parameters
        sys.argv[?] (--dt)     delay time (hours)
        '''
        if len(sys.argv) < 2:
            print('Please provide a file name.')
            sys.exit()
        availableShortOptions = ""
        availableLongOptions = ["nrmfl", "linux",
                                "rc", "hd=", "nacs", "gpu", "sp", "dt="]
        try:
            opts, args = getopt.getopt(
                sys.argv[2:], availableShortOptions, availableLongOptions)
        except getopt.GetoptError:
            print('Parameter error.')
            print('Available short options: ' + availableShortOptions)
            print('sys.argv[2:]', sys.argv[2:])
            try:
                print('opts', opts)
                print('args', args)
            except:
                pass
            sys.exit()

        # help info
        if sys.argv[1:] != []:
            if '--help' in sys.argv[1]:
                print('\nUsage:')
                print(f'python {sys.argv[0]} <file_name> [options]')
                print('\nPurpose:')
                print('1. Re-encode video files for unified video and audio codec.')
                print('2. Reduce file size with CPU compute.')
                print('\nInfo:')
                print('CPU compute: Slow, dynamic encoding, reduce file size.')
                print('GPU compute: Fast, static encoding, increase file size.')
                print('\nArguments:')
                print('sys.argv[1] path and name to the video file log')
                print(
                    'sys.argv[?] (--nrmfl)  not remove file list of processed files')
                print('sys.argv[?] (--linux)  linux os')
                print('sys.argv[?] (--rc)     recycle old video')
                print('sys.argv[?] (--hd 0)   hidden file info + length + ETA')
                print('sys.argv[?] (--hd 1)   hidden file info')
                print('sys.argv[?] (--nacs)   not auto clear screen')
                print('sys.argv[?] (--gpu)    use gpu')
                print('sys.argv[?] (--sp)     show parameters')
                print('sys.argv[?] (--dt)     delay time (hours)')
                print('\n')
                sys.exit()

        # initialize variables
        self.file_name = sys.argv[0]
        self.file_path = sys.argv[1]
        self.log_remove = True
        self.shell = False
        self.del_old = True
        self.h0 = True
        self.h1 = True
        self.ac = True
        self.gpu = False
        self.delay_time = 0

        # check for parameters
        for opt, arg in opts:
            if opt in ('--nrmfl'):
                self.log_remove = False
            if opt in ('--linux'):
                self.shell = True
            if opt in ('--rc'):
                self.del_old = False
            if opt in ('--hd'):
                if arg == '0':
                    self.h0 = False
                if arg == '1':
                    self.h1 = False
            if opt in ('--nacs'):
                self.ac = False
            if opt in ('--gpu'):
                self.gpu = True
            if opt in ('--sp'):
                show = True
            if opt in ('--dt'):
                self.delay_time = float(arg)

        # op based parameters
        if self.shell:
            self.record_path = os.path.dirname(self.file_path) + "/record.txt"
        else:
            self.record_path = os.path.dirname(self.file_path) + "\\record.txt"

        # display parameters
        if show:
            print('Parameters status:\n')
            print('file_name: ' + self.file_name)
            print('file_path: ' + self.file_path)
            print('record_path: ' + self.record_path)
            print('-nrmfl: ' + str(not self.log_remove))
            print('-linux: ' + str(self.shell))
            print('-rc: ' + str(not self.del_old))
            print('-hd 0: ' + str(not self.h0))
            print('-hd 1: ' + str(not self.h1))
            print('-nacs: ' + str(not self.ac))
            print('-gpu: ' + str(self.gpu))
            print('-sp: ' + str(show))
            print('-dt: ' + str(self.delay_time))
            print('\n')
            if input('Enter [y] to continue... ') != 'y':
                print('\nExit.')
                sys.exit()
            if self.shell:
                os.system('clear')
            else:
                os.system('cls')

        # sleep
        if self.delay_time > 0:
            wait_seconds = self.delay_time * 3600
            start = timeit.default_timer()
            while timeit.default_timer() - start < wait_seconds:
                time.sleep(1)
                print(
                    f'Waited {round((timeit.default_timer() - start)/3600, 4)}/{self.delay_time} hours...', end='\r')
        else:
            pass

        # start the timer
        self.start_time = timeit.default_timer()

    def read_log(self):
        # get the log file contents
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()

    def remove_identical_lines(self):
        # remove identical lines
        pass

    def compress(self):
        def f1():
            '''
            show progress and file info
            '''
            try:
                self.video_path = self.lines[0]
            except IndexError:
                print('{0} >> {1} >> No more videos to compress'.format(
                    self.file_name, currenttime()))
                return 1
            self.video_path = self.video_path.replace('\n', '')
            filtype = os.path.splitext(self.video_path)[1]
            filename = os.path.splitext(self.video_path)[0] + '_temp'
            self.nvideo_path = filename + filtype
            self.video_path = str(Path(self.video_path))
            self.nvideo_path = str(Path(self.nvideo_path))
            print('{0} >> {1} >> progress: {2}/{3} {4}%'.format(
                self.file_name, currenttime(), self.progress, self.total, format(self.progress/self.total*100, '.2f')))
            if self.h0 and self.h1:
                print('{0} >> {1} >> video_path: {2}'.format(
                    self.file_name, currenttime(), self.video_path))
                print('{0} >> {1} >> temp_path: {2}'.format(
                    self.file_name, currenttime(), self.nvideo_path))

        def f2():
            '''
            check file existance
            '''
            exist = os.path.isfile(self.video_path)
            if not exist:
                l = '{0} >> {1} >> {2} doesn\'t exist'.format(
                    self.file_name, currenttime(), self.video_path)
                print(l)
                with open(self.record_path, 'a', encoding='utf-8') as f:
                    f.write(l + '\n')
                self.lines.pop(0)
                return 1
            if self.h0 and self.h1:
                print('{0} >> {1} >> processing {2}'.format(
                    self.file_name, currenttime(), os.path.basename(self.video_path)))

        def f3():
            '''
            calculate ETA & display uptime
            '''
            time_temp = timeit.default_timer() - self.start_time
            uptime = s2strdhms(time_temp)
            if self.progress == 1:
                eta = 'N/A'
            else:
                eta = time_temp/(self.progress-1)*self.total - time_temp
                eta = s2strdhms(eta)
            if self.h0:
                print('{0} >> {1} >> uptime: {2}'.format(
                    self.file_name, currenttime(), uptime))
                print('{0} >> {1} >> ETA: {2}'.format(
                    self.file_name, currenttime(), eta))

        def f4():
            '''
            get video duration
            '''
            ffprobe_cmd = 'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{0}"'.format(
                self.video_path)
            duration = ((subprocess.check_output(
                ffprobe_cmd, shell=self.shell)).decode('utf-8')).replace('\r\n', '')
            duration = s2strdhms(float(duration))
            if self.h0:
                print('{0} >> {1} >> duration: {2}'.format(
                    self.file_name, currenttime(), duration))

        def f5():
            '''
            get video frame count
            '''
            # # removed because it's too slow
            ffprobe_cmd = 'ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 "{0}"'.format(
                self.video_path)
            frame_count = int((subprocess.check_output(
                ffprobe_cmd, shell=self.shell)).decode('utf-8'))
            if self.h0:
                print('{0} >> {1} >> frame count: {2}'.format(
                    self.file_name, currenttime(), frame_count))

        def f6():
            '''
            get video size pre-compression
            '''
            ffprobe_cmd = 'ffprobe -v error -show_entries format=size -of default=nokey=1:noprint_wrappers=1 "{0}"'.format(
                self.video_path)
            self.prepsize = int((subprocess.check_output(
                ffprobe_cmd, shell=self.shell)).decode('utf-8'))

        def f7():
            '''
            compress video
            '''
            if self.gpu:
                # really bad quality, can't be modified or improved, due to the nature of the codec (hardware accelerated)
                # https://video.stackexchange.com/questions/29659/is-there-a-way-to-improve-h264-nvenc-output-quality
                ffmpeg_cmd = 'ffmpeg -v quiet -stats -y -i "{0}" -vcodec h264_nvenc -b:v 0 -acodec aac "{1}"'.format(
                    self.video_path, self.nvideo_path)
            else:
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
            if self.h0 and self.h1:
                print('{0} >> {1} >> compressed {2}'.format(
                    self.file_name, currenttime(), os.path.basename(self.nvideo_path)))

        def f8():
            '''
            recycle / delete old video
            '''
            if self.del_old:
                os.remove(self.video_path)
            else:
                send2trash(self.video_path)
            if self.h0 and self.h1:
                if self.del_old:
                    print('{0} >> {1} >> deleted {2}'.format(
                        self.file_name, currenttime(), os.path.basename(self.video_path)))
                else:
                    print('{0} >> {1} >> recycled {2}'.format(
                        self.file_name, currenttime(), os.path.basename(self.video_path)))

        def f9():
            '''
            rename new video
            '''
            os.rename(self.nvideo_path, self.video_path)
            if self.h0 and self.h1:
                print('{0} >> {1} >> renamed {2}'.format(
                    self.file_name, currenttime(), os.path.basename(self.nvideo_path)))

        def f10():
            '''
            get post-compression video size
            '''
            ffprobe_cmd = 'ffprobe -v error -show_entries format=size -of default=nokey=1:noprint_wrappers=1 "{0}"'.format(
                self.video_path)
            self.postpsize = int((subprocess.check_output(
                ffprobe_cmd, shell=self.shell)).decode('utf-8'))

        def f11():
            '''
            calculate compression ratio / size reduction
            '''
            percentage = self.postpsize/self.prepsize*100
            if percentage < 10:
                percentage = '  ' + str(format(percentage, '.4f'))
            elif percentage < 100:
                percentage = ' ' + str(format(percentage, '.4f'))
            else:
                percentage = str(format(percentage, '.4f'))
            saved = format((self.prepsize-self.postpsize)/(2**23), '10.4f')
            if self.h0 and self.h1:
                l = '{0} >> {1} >> ratio: {2}% >> saved {3}MB >> compressed {4}'.format(
                    self.file_name, currenttime(), percentage, saved, os.path.basename(self.video_path))
                print(l)
            l = '{0} >> {1} >> ratio: {2}% >> saved {3}MB >> compressed {4}'.format(
                self.file_name, currenttime(), percentage, saved, self.video_path)
            with open(self.record_path, 'a', encoding='utf-8') as f:
                f.write(l + '\n')

        def f12():
            '''
            remove line from log file
            '''
            try:
                self.lines.pop(0)
            except Exception as e:
                print('{0} >> {1} >> exception: {2}'.format(
                    self.file_name, currenttime(), e))
            if self.log_remove:
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    f.writelines(self.lines)
            if self.progress >= self.total:
                return 1
            print()

        self.progress = 0
        self.total = len(self.lines)
        while True:
            if self.ac:
                if self.shell:
                    os.system('clear')
                else:
                    os.system('cls')
            self.progress += 1
            if f1() == 1:
                break
            if f2() == 1:
                continue
            f3()
            f4()
            # f5()
            f6()
            f7()
            f8()
            f9()
            f10()
            f11()
            if f12() == 1:
                break

        # end
        print('\n{0} >> {1} >> finished compressing all designated files.'.format(
            self.file_name, currenttime()))


# main
if __name__ == '__main__':
    cv = compress_video()
    cv.read_log()
    cv.remove_identical_lines()
    cv.compress()
