import subprocess


class Manipulator:

    __ward_file: str = ""

    def _rec_ward_name(self, ward_name: str):
        self.__ward_file = ward_name

    def copy_file(self, name_file):
        new_name: str = name_file.split('.')[0] + "_run.py"
        subprocess.run(["cp", f"{name_file}", f"{new_name}"])
        self._rec_ward_name(new_name)

    def make_shell_accessible(self):
        wizardry_bash = "#!/usr/bin/python3"
        if self.__ward_file:
            with open(self.__ward_file, "r") as f:
                temp_data = f.read()
            with open(self.__ward_file, "w") as f:
                f.writelines(wizardry_bash + "\n")
                f.write(temp_data)
        else:
            print("Can't work")

    def setting_permissions(self):
        if self.__ward_file:
            print(self.__ward_file)
            subprocess.run(["sudo", "-S", "chmod", "500", self.__ward_file])
        else:
            print("Can't work")


def main():
    manipulator = Manipulator()
    manipulator.copy_file("dz1_1.py")
    manipulator.make_shell_accessible()
    manipulator.setting_permissions()


if __name__ == '__main__':
    main()
