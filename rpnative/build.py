import os
import platform
import subprocess
import sys


class chdir(object):
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.cwd = os.getcwd()
        os.chdir(self.path)

    def __exit__(self, *args, **kwargs):
        os.chdir(self.cwd)


def main():
    build_dir = 'build'

    with chdir(build_dir):
        kwargs = {
            'stderr': sys.stderr,
            'stdout': sys.stdout,
        }

        subprocess.run(['cmake', '-DCMAKE_INSTALL_PREFIX=..', '..'], **kwargs)

        if platform.system() == 'Windows':
            subprocess.run(['nmake'], **kwargs)
            subprocess.run(['nmake', 'install'], **kwargs)
        else:
            subprocess.run(['make'], **kwargs)
            subprocess.run(['make', 'install'], **kwargs)


if __name__ == '__main__':
    main()
