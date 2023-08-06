import os

from trashcli.put.ensure_dir import EnsureDir
from trashcli.put.fs import Fs
from trashcli.put.info_dir import InfoDir
from trashcli.put.path_maker import PathMaker
from trashcli.put.reporter import TrashPutReporter
from trashcli.put.security_check import SecurityCheck
from trashcli.put.trash_dir_volume import TrashDirVolume
from trashcli.put.trash_directory_for_put import TrashDirectoryForPut


class TrashFileIn:
    def __init__(self,
                 fs,  # type: Fs
                 reporter,  # type: TrashPutReporter
                 info_dir,  # type: InfoDir
                 trash_dir,  # type: TrashDirectoryForPut
                 trash_dir_volume,  # type: TrashDirVolume
                 ensure_dir,  # type: EnsureDir
                 ):
        self.reporter = reporter
        self.path_maker = PathMaker()
        self.security_check = SecurityCheck(fs)
        self.info_dir = info_dir
        self.trash_dir = trash_dir
        self.trash_dir_volume = trash_dir_volume
        self.ensure_dir = ensure_dir

    def trash_file_in(self,
                      path,
                      trash_dir_path,
                      volume,
                      path_maker_type,
                      check_type,
                      file_has_been_trashed,
                      volume_of_file_to_be_trashed,
                      program_name,
                      verbose,
                      environ,
                      ):  # type: (...) -> bool
        norm_trash_dir_path = os.path.normpath(trash_dir_path)
        trash_dir_is_secure, messages = self.security_check. \
            check_trash_dir_is_secure(norm_trash_dir_path,
                                      check_type)
        self.reporter.log_info_messages(messages, program_name, verbose)

        if trash_dir_is_secure:
            volume_of_trash_dir = self.trash_dir_volume. \
                volume_of_trash_dir(trash_dir_path)
            self.reporter.trash_dir_with_volume(norm_trash_dir_path,
                                                volume_of_trash_dir,
                                                program_name, verbose)
            if self._file_could_be_trashed_in(
                    volume_of_file_to_be_trashed,
                    volume_of_trash_dir):
                try:
                    self.ensure_dir.ensure_dir(trash_dir_path, 0o700)
                    self.ensure_dir.ensure_dir(
                        os.path.join(trash_dir_path, 'files'),
                        0o700)
                    self.trash_dir.trash2(path, program_name, verbose,
                                          path_maker_type, volume,
                                          trash_dir_path)
                    self.reporter.file_has_been_trashed_in_as(
                        path,
                        norm_trash_dir_path,
                        program_name,
                        verbose,
                        environ)
                    file_has_been_trashed = True

                except (IOError, OSError) as error:
                    self.reporter.unable_to_trash_file_in_because(
                        path, norm_trash_dir_path, error, program_name, verbose,
                        environ)
            else:
                self.reporter.wont_use_trash_dir_because_in_a_different_volume(
                    path, norm_trash_dir_path, volume_of_file_to_be_trashed,
                    volume_of_trash_dir, program_name, verbose, environ)
        else:
            self.reporter.trash_dir_is_not_secure(norm_trash_dir_path,
                                                  program_name, verbose)
        return file_has_been_trashed

    def _file_could_be_trashed_in(self,
                                  volume_of_file_to_be_trashed,
                                  volume_of_trash_dir):
        return volume_of_trash_dir == volume_of_file_to_be_trashed
