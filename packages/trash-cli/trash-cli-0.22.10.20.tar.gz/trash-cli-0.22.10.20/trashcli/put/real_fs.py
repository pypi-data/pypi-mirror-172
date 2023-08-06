import os
import stat

from trashcli import fs
from trashcli.fs import write_file
from trashcli.put.fs import Fs


class RealFs(Fs):

    @staticmethod
    def atomic_write(path, content):
        fs.atomic_write(path, content)

    @staticmethod
    def chmod(path, mode):
        os.chmod(path, mode)

    @staticmethod
    def isdir(path):
        return os.path.isdir(path)

    @staticmethod
    def isfile(path):
        return os.path.isfile(path)

    @staticmethod
    def getsize(path):
        return os.path.getsize(path)

    @staticmethod
    def exists(path):
        return os.path.exists(path)

    @staticmethod
    def makedirs(path, mode):
        os.makedirs(path, mode)

    @staticmethod
    def move(path, dest):
        return fs.move(path, dest)

    @staticmethod
    def remove_file(path):
        fs.remove_file(path)

    @staticmethod
    def islink(path):
        return os.path.islink(path)

    @staticmethod
    def has_sticky_bit(path):
        return (os.stat(path).st_mode & stat.S_ISVTX) == stat.S_ISVTX

    @staticmethod
    def realpath(path):
        return os.path.realpath(path)

    @staticmethod
    def is_accessible(path):
        return os.access(path, os.F_OK)

    @staticmethod
    def make_file(path, content):
        write_file(path, content)

    def get_mod(self, path):
        return stat.S_IMODE(os.lstat(path).st_mode)
