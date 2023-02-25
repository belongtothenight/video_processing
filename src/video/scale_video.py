import sys
import subprocess
import os
import getopt
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


class bcolors:
    # https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class compress_video():
    def __init__(self):
        '''
        Parameters:
        == COMMAND ===========================================================
        --help: help
        == SYSTEM =============================================================
        --linux: use linux shell
        == DISPLAY ============================================================
        --hd: hide display 
            0: hide the video path
            1: hide the progress
        --cs: clear screen
        --icf: input confirmation
        == FILE ===============================================================
        --kl: keep log
            keep the log file after the video is scaled
        --rov: recycle old video
            recycle the original video after the video is scaled
        sys.argv[1]: the path of the log file (contains the video paths, required)
        == SCALE ==============================================================
        sys.argv[2]: the scale of the video is going to scale to (ex 1920x1080 , required)
        sys.argv[3]: the algorithm of the video is going to scale with (bilinear/bicubic/lanczos, required)
        '''
        # short options (limited to one character, -h -> "h:")
        availableShortOptions = ""
        # long options (no limit, --help -> ["help"])
        availableLongOptions = ['help', 'linux',
                                'hd=', 'cs', 'icf', 'kl', 'rov']
        try:
            opts, args = getopt.getopt(
                sys.argv[4:], availableShortOptions, availableLongOptions)
        except getopt.GetoptError:
            print(bcolors.WARNING + '>> CLI Parameter error.' + bcolors.ENDC)
            sys.exit()
        # print(opts)
        # print(args)

        # help message
        helpMessage = '\
        Parameters:\n\
        == COMMAND ===========================================================\n\
        --help: help\n\
        == SYSTEM =============================================================\n\
        --linux: use linux shell\n\
        == DISPLAY ============================================================\n\
        --hd: hide display\n\
            0: hide the video path\n\
            1: hide the progress\n\
        --cs: clear screen\n\
        --icf: input confirmation\n\
        == FILE ===============================================================\n\
        --kl: remove log\n\
            remove the log file after the video is scaled\n\
        --rov: recycle old video\n\
            recycle the original video after the video is scaled\n\
        sys.argv[1]: the path of the log file (contains the video paths, required)\n\
        == SCALE ==============================================================\n\
        sys.argv[2]: the scale of the video is going to scale to (ex 1920x1080 , required)\n\
        sys.argv[3]: the algorithm of the video is going to scale with (bilinear/bicubic/lanczos, required)\n\
        '
        if opts != []:
            if '--help' in opts[0]:
                print('Help message:\n')
                print(helpMessage)
                sys.exit()

        # initialize variables
        self.fileName = sys.argv[0]
        self.filePath = sys.argv[1]
        self.scale = sys.argv[2]
        self.algorithm = sys.argv[3]
        self.keepLog = False
        self.shell = False
        self.recycleOldVid = False
        self.h0 = False
        self.h1 = False
        self.clearScreen = False
        self.inputConfirmation = False

        # validate parameters
        try:
            h, w = self.scale.split('x')
            h = int(h)
            w = int(w)
        except:
            print(bcolors.WARNING + '>> Scale parameter error.' + bcolors.ENDC)
            sys.exit()
        if self.algorithm not in ['bilinear', 'bicubic', 'lanczos']:
            print(bcolors.WARNING + '>> Algorithm parameter error.' + bcolors.ENDC)
            sys.exit()

        # check for parameters
        for opt, arg in opts:
            if opt == '--linux':
                self.shell = True
            if opt == '--hd':
                if arg == '0':
                    self.h0 = True
                if arg == '1':
                    self.h1 = True
            if opt == '--cs':
                self.clearScreen = True
            if opt == '--icf':
                self.inputConfirmation = True
            if opt == '--kl':
                self.keepLog = True
            if opt == '--rov':
                self.recycleOldVid = True

        # op based parameters
        if self.shell:
            self.recordPath = os.path.dirname(self.filePath) + "/record.txt"
        else:
            self.recordPath = os.path.dirname(self.filePath) + "\\record.txt"

        # display parameters
        if self.inputConfirmation:
            print('\nParameters status:\n')
            print('linux: ' + str(self.shell))
            print('hd: (0)' + str(self.h0) + '/(1)' + str(self.h1))
            print('clearScreen: ' + str(self.clearScreen))
            print('keepLog: ' + str(self.keepLog))
            print('recycleOldVid: ' + str(self.recycleOldVid))
            print('filePath: ' + self.filePath)
            print('recordPath: ' + self.recordPath)
            print('scale: ' + self.scale)
            print('algorithm: ' + self.algorithm)
            if input('\nEnter [y] to continue... ') != 'y':
                print(bcolors.OKBLUE + '\nExit.\n' + bcolors.ENDC)
                sys.exit()

        # clear screen
        if self.clearScreen:
            if self.shell:
                os.system('clear')
            else:
                os.system('cls')

        # opposite of parameters
        self.h0 = not self.h0
        self.h1 = not self.h1
        self.recycleOldVideo = not self.recycleOldVid
        self.keepLog = not self.keepLog

        # start the timer
        self.start_time = timeit.default_timer()

    def read_log(self):
        # get the log file contents
        with open(self.filePath, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()

    def remove_identical_lines(self):
        # remove identical lines
        pass

    def process(self, test=False):
        def f1():
            '''
            show progress and file info
            '''
            try:
                self.video_path = self.lines[0]
            except IndexError:
                print('{0} >> {1} >> No more videos to process'.format(
                    self.fileName, currenttime()))
                return 1
            self.video_path = self.video_path.replace('\n', '')
            filtype = os.path.splitext(self.video_path)[1]
            filename = os.path.splitext(self.video_path)[0] + '_temp'
            self.nvideo_path = filename + filtype
            self.video_path = str(Path(self.video_path))
            self.nvideo_path = str(Path(self.nvideo_path))
            print('{0} >> {1} >> progress: {2}/{3} {4}%'.format(
                self.fileName, currenttime(), self.progress, self.total, format(self.progress/self.total*100, '.2f')))
            if self.h0 and self.h1:
                print('{0} >> {1} >> video_path: {2}'.format(
                    self.fileName, currenttime(), self.video_path))
                print('{0} >> {1} >> temp_path: {2}'.format(
                    self.fileName, currenttime(), self.nvideo_path))

        def f2():
            '''
            check file existance
            '''
            exist = os.path.isfile(self.video_path)
            if not exist:
                l = '{0} >> {1} >> {2} doesn\'t exist'.format(
                    self.fileName, currenttime(), self.video_path)
                print(l)
                with open(self.recordPath, 'a', encoding='utf-8') as f:
                    f.write(l + '\n')
                self.lines.pop(0)
                return 1
            if self.h0 and self.h1:
                print('{0} >> {1} >> processing {2}'.format(
                    self.fileName, currenttime(), os.path.basename(self.video_path)))

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
                    self.fileName, currenttime(), uptime))
                print('{0} >> {1} >> ETA: {2}'.format(
                    self.fileName, currenttime(), eta))

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
                    self.fileName, currenttime(), duration))

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
                    self.fileName, currenttime(), frame_count))

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
            process video
            '''
            ffmpeg_cmd = 'ffmpeg -v quiet -stats -y -i "{0}" -vf scale={1}:flags={2} "{3}"'.format(
                self.video_path, self.scale, self.algorithm, self.nvideo_path)
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
                    self.fileName, currenttime(), os.path.basename(self.nvideo_path)))

        def f8():
            '''
            recycle / delete old video
            '''
            if not self.recycleOldVid:
                os.remove(self.video_path)
                if self.h0 and self.h1:
                    print('{0} >> {1} >> deleted {2}'.format(
                        self.fileName, currenttime(), os.path.basename(self.video_path)))
            else:
                send2trash(self.video_path)
                if self.h0 and self.h1:
                    print('{0} >> {1} >> recycled {2}'.format(
                        self.fileName, currenttime(), os.path.basename(self.video_path)))

        def f9():
            '''
            rename new video
            '''
            os.rename(self.nvideo_path, self.video_path)
            if self.h0 and self.h1:
                print('{0} >> {1} >> renamed {2}'.format(
                    self.fileName, currenttime(), os.path.basename(self.nvideo_path)))

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
            calculate before/after size ratio
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
                l = '{0} >> {1} >> scaled {4}'.format(
                    self.fileName, currenttime(), percentage, saved, os.path.basename(self.video_path))
                print(l)
            l = '{0} >> {1} >> scaled {4}'.format(
                self.fileName, currenttime(), percentage, saved, self.video_path)
            with open(self.recordPath, 'a', encoding='utf-8') as f:
                f.write(l + '\n')

        def f12():
            '''
            remove line from log file
            '''
            try:
                self.lines.pop(0)
            except Exception as e:
                print('{0} >> {1} >> exception: {2}'.format(
                    self.fileName, currenttime(), e))
            if test:
                self.keepLog = False
            if self.keepLog:
                with open(self.filePath, 'w', encoding='utf-8') as f:
                    f.writelines(self.lines)

            if self.progress >= self.total:
                return 1
            print()
            if self.clearScreen:
                if self.shell:
                    os.system('clear')
                else:
                    os.system('cls')

        self.progress = 0
        self.total = len(self.lines)
        while True:
            self.progress += 1
            if f1() == 1:
                break
            if f2() == 1:
                continue
            f3()
            f4()
            # f5()
            # f6()
            f7()
            if not test:
                f8()
                f9()
            # f10()
            # f11()
            if f12() == 1:
                break

        # end
        print('\n{0} >> {1} >> finished compressing all designated files.'.format(
            self.fileName, currenttime()))


# main
if __name__ == '__main__':
    cv = compress_video()
    cv.read_log()
    # cv.remove_identical_lines()
    cv.process()
