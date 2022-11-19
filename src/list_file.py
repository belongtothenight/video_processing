import os
import pathlib


class export_file_log():
    def __init__(self):
        while True:
            dir = input('Enter the path to the root of exporting files: ')
            self.dir = pathlib.Path(dir)
            path = input('Enter the path to export file log: ')
            self.path = pathlib.Path(path)
            format = input('Enter the format of files to export: ')
            self.format = format
            print()
            print('Root of exporting files: ' + str(self.dir))
            print('Export file log path: ' + str(self.path))
            print('Format of files to export: ' + self.format)
            print()
            if input('Is this correct? (y/n): ') == 'y':
                break

    def export(self):
        print('Exporting...')
        for file in self.dir.rglob('*'):
            file = pathlib.Path(file)
            if file.is_file():
                ext = (os.path.splitext(
                    os.path.basename(file))[1]).lstrip('.')
                if ext == self.format:
                    print('\t\t\t\t\t\t\t\t', end='\r')
                    print(file, end='\r')
                    with open(self.path, 'a', encoding='utf-8') as f:
                        f.write(str(file) + '\n')


if __name__ == '__main__':
    os.system('cls')
    while True:
        try:
            efl = export_file_log()
            efl.export()
        except Exception as e:
            print(e)
        print('\n\n')
        con = input('Continue? (y/n): ')
        if con == 'n':
            break
