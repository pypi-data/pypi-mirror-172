import sys
import os
import stat
import time
from colorama import Fore, Style, init, deinit


class Ls:
    '''
    This is a simple Python class for listing the content of a directory.
    The sole purpose is giving better visualization.
    '''

    __slots__ = 'opt', 'path', 'just'

    def __init__(self, opt='', path='.', just=7) -> None:

        if not opt or opt.startswith('-'):
            self.opt, self.path = opt, path
        else:
            self.opt, self.path = '', opt
        self.just = just

    def echo(self, signal: int) -> None:
        try:
            with os.scandir(self.path) as dir:
                dir = sorted(dir, key=lambda x: (x.stat().st_mode, x.name))

                if 'l' in self.opt:
                    for i in dir:
                        filemode_str = self._windows_filemode(
                                i.stat().st_file_attributes, 'c' in self.opt)
                        if (i.name.startswith('.')
                           or 'h' in filemode_str) and 'a' not in self.opt:
                            continue

                        # print() by 'column item' for better performance
                        print(end=' ')
                        print(filemode_str, end='   ')
                        print(time.strftime(
                            '%d %b %y %H:%M', time.localtime(
                                i.stat().st_ctime)), end='   ')
                        print(self._human_color(
                            self._humanize(i), 'c' in self.opt).rjust(
                                self.just), end='   ')
                        print(self._type_color(i, 'c' in self.opt))

                else:
                    print(*[self._type_color(i, 'c' in self.opt) for i in dir
                          if not i.name.startswith('.')
                          or 'a' in self.opt], sep='   ')

        except NotADirectoryError:
            print(f'{self.path} is not a directory')
        except FileNotFoundError as err:
            print(err)
        except PermissionError as err:
            if signal:  # not going recursively on echo()
                print(f'{str(err)[:12]} {err.strerror}: {err.filename}')
                deinit()
                quit()

            self.path = os.path.realpath(self.path)
            self.echo(1)
            print(Style.RESET_ALL +
                  "\nYou can't access files from here because CD doesn't "
                  f"follow symlinks. Do first: cd {os.path.realpath('.')}"
                  )

    def _type_color(self, i: os.DirEntry, colors: bool) -> str:
        if not colors:
            return i.name

        # if i.is_symlink(): doesn't work
        if i.is_dir():
            # workaround
            if os.path.realpath(i.path) != os.path.join(os.path.realpath(self.path), i.name):  # noqa: E501
                return (Fore.CYAN
                        + i.name
                        + Fore.LIGHTBLACK_EX
                        + ' --> '
                        + os.path.realpath(i.path)
                        + Style.RESET_ALL)

            return Fore.LIGHTBLUE_EX + i.name + Style.RESET_ALL

        else:
            if i.name.endswith(('.zip', '.exe', '.msi', '.dll',
                                '.bat', '.sys', '.log', '.ini')):
                return Fore.YELLOW + i.name + Style.RESET_ALL
            if i.name.endswith(('.py', '.pyx', '.pyd', '.pyw')):
                return Fore.GREEN + i.name + Style.RESET_ALL
            if i.name.endswith(('.tmp')):
                return Fore.LIGHTBLACK_EX + i.name + Style.RESET_ALL
            if i.name.endswith(('.pdf')):
                return Fore.LIGHTRED_EX + i.name + Style.RESET_ALL
            return i.name

    def _humanize(self, i: os.DirEntry):
        if i.is_dir():
            return '-'

        entry = i.stat().st_size
        units = ('k', 'M', 'G')
        final = ''

        for unit in units:
            if entry >= 1024:
                entry /= 1024
                final = unit
            else:
                break

        if entry:
            if final:
                return f'{entry:.1f}{final}'
            return str(entry)
        return '-'

    def _human_color(self, data: str, colors: bool) -> str:
        if not colors:
            return data

        self.just = 16

        if 'G' in data:
            return Fore.RED + data + Style.RESET_ALL
        elif 'M' in data:
            return Fore.LIGHTRED_EX + data + Style.RESET_ALL
        elif 'k' in data:
            return Fore.YELLOW + data + Style.RESET_ALL
        else:
            return Fore.WHITE + data + Style.RESET_ALL

    def _windows_filemode(
        self,
        data: os.stat_result.st_file_attributes,
        colors: bool
    ):

        str_res = ''
        checks = (('a', stat.FILE_ATTRIBUTE_ARCHIVE),
                  ('d', stat.FILE_ATTRIBUTE_DIRECTORY),
                  ('h', stat.FILE_ATTRIBUTE_HIDDEN),
                  ('r', stat.FILE_ATTRIBUTE_READONLY))

        for check in checks:
            str_res = str_res + check[0] if data == check[1] else str_res + '-'

        # only if we haven't a perfect match
        if str_res == '----':
            str_res = ''
            for check in checks:
                if data >= check[1]:
                    str_res += check[0]
                    data -= check[1]
                else:
                    str_res += '-'
            else:
                # something went wrong if there's still `data`
                if data:
                    str_res = '---*'

        if not colors:
            return str_res

        for char in 'adhr':
            if char in str_res:
                str_res = (str_res[:str_res.index(char)]
                           + Fore.BLUE
                           + char
                           + Style.RESET_ALL
                           + str_res[str_res.index(char)+1:])

        return str_res


def main():
    init()

    args = sys.argv[1:]

    # notice useless parameters
    if len(args) > 2:
        print(f'Ignored {args[2:]} parameter(s)')
        args = args[:2]
    if len(args) == 2 and not args[0].startswith('-'):
        print('Try: py ls.py -acl path')

    Ls(*args).echo(0)
    deinit()


if __name__ == '__main__':
    main()
