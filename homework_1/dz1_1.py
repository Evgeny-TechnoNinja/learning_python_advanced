import os
import subprocess
import calendar
import datetime
from typing import Union
from random import sample


class Manager:
    """
    Interacts with the system, runs orders
    """

    def __init__(self, working_directory: str):
        """
        :param working_directory: directory name for main job
        """
        self._working_directory = working_directory

    def get_name_working_directory(self) -> str:
        return self._working_directory

    def checking_work_directory(self):
        return os.path.exists(self._working_directory)

    def _switch_working_directory(self):
        os.chdir(self._working_directory) if self.checking_work_directory() else print("Directory not created")

    def _level_up_directory(self):
        os.chdir("..") if os.getcwd().split("/")[-1] == self._working_directory else print("Can't work, I'm not your directory") # noqa

    def create_files(self):
        self._switch_working_directory()
        file_names = self.get_files(".")
        if os.getcwd().split("/")[-1] == self._working_directory and len(file_names) == 0:
            for current_day in self.date_generator():
                file_name = current_day + ".log"
                self.executor(["touch", file_name])
            self._level_up_directory()
        else:
            print("Files not created")
            self._level_up_directory()

    def change_owners(self, user_owners: str, group_owners: str, type_work: str):
        if type_work == "files":
            self._switch_working_directory()
            file_names = self.get_files(".")
            if len(file_names) > 0:
                for file_name in file_names:
                    self.executor(["sudo", "-S", "chown", f"{user_owners}:{group_owners}", f"{file_name}"])
            else:
                print("No files, can't work")
            self._level_up_directory()
        elif type_work == "directory":
            check: bool = self.checking_work_directory()
            if check:
                directory_name = self.get_name_working_directory()
                self.executor(["sudo", "-S", "chown", f"{user_owners}:{group_owners}", f"{directory_name}"])
            else:
                print("No directory, I can't work")
        else:
            print("type of work unknown, can't work")

    def delete_random_files(self):
        check: bool = self.checking_work_directory()
        if check:
            self._switch_working_directory()
            file_names = self.get_files(".")
            try:
                victims = sample(file_names, 5)
                order = ["sudo", "-S", "rm", *victims]
                self.executor(order)
                print("Files have been deleted: {}".format(" ".join(victims)))
            except ValueError:
                print("No data to work")
            finally:
                self._level_up_directory()
        else:
            print("No working directory")

    @staticmethod
    def get_files(path: str) -> list:
        return os.listdir(path=path)

    @staticmethod
    def date_generator():
        date = datetime.datetime.now()
        last_day = calendar.monthrange(date.year, date.month)[1]
        for day in range(1, last_day):
            yield f"{day}-{date.month}-{date.year}"

    @staticmethod
    def executor(commands: Union[str, list]):
        """
        executes commands for the system
        :param commands: can be represented as a string or a list of strings
        """
        try:
            subprocess.run(commands)
        except Exception as error:
            print(error)
            print("Incorrect data, enter the correct command")


def main():
    worker = Manager("dz1")
    worker.executor("whoami")
    worker.executor("pwd")
    folder = worker.get_name_working_directory()
    worker.executor(["mkdir", "-p", folder])
    worker.create_files()
    worker.change_owners("root", "root", "files")
    worker.change_owners("root", "root", "directory")
    worker.delete_random_files()


if __name__ == '__main__':
    main()
