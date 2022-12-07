from typing import List
import base64
import re


def write_output(file: str, value: str):
    print(f"{value}")
    with open(file, "wb") as output:
        out = base64.b64encode(f"{value}".encode("utf8"))
        output.write(out)


input_file = "./input.txt"
# input_file = "./test_input.txt"
output_file1 = "./output1.txt"
output_file2 = "./output2.txt"


# Example file system.
filesystem = {"/": [{"a": 123}, {"b": 123}], "/abc": [{"a": 123}, {"b": 123}]}


class Filesystem:
    __total_size = "__total_size__"
    __total_deep_size = "__total_deep_size__"

    def __init__(self):
        self.current_path = "/"
        self.filesystem = {"/": {self.__total_size: 0, self.__total_deep_size: 0}}

    def ls(self):
        """
        Get the files and directories of the current directory.
        """
        dirs = self.find_current_dirs()
        for dir in dirs:
            print(dir)

        files = self.filesystem[self.current_path].keys()

        for file in files:
            if file == self.__total_size:
                continue
            print(f"{self.filesystem[self.current_path][file]} {file}")

    def write_file(self, name: str, size: int):
        """Add files from construction"""
        self.filesystem[self.current_path][name] = size
        self.filesystem[self.current_path][self.__total_size] += size
        self._add_to_deep_size(size)

    def _add_to_deep_size(self, size: int):
        """Add size to all dirs in the path chain"""
        if self.current_path == "/":
            self.filesystem["/"][self.__total_deep_size] += size
        else:
            current_dir = "/"
            dirs = self.current_path.split("/")
            for d in dirs:
                if current_dir != "/":
                    current_dir += "/"
                current_dir += d
                self.filesystem[current_dir][self.__total_deep_size] += size

    def write_dir(self, name: str):
        """Write in directory names"""
        self.filesystem[f"{self.current_path}{self._slash_if_needed()}{name}"] = {
            self.__total_size: 0,
            self.__total_deep_size: 0,
        }

    def _slash_if_needed(self):
        return "/" if self.current_path != "/" else ""

    def cd(self, dir: str):
        """
        Change the current directory.
        .. = go back one.
        """
        if dir == "..":
            if self.current_path == "/":
                pass
            self.current_path = "/".join(self.current_path.split("/")[:-1])
        elif dir == "/":
            self.current_path == "/"
        else:
            prefix = "/"
            if self.current_path == "/":
                prefix = ""
            self.current_path += f"{prefix}{dir}"

    def find_current_dirs(self):
        dirs = []
        for key in self.filesystem.keys():
            if re.match(
                rf"{self.current_path}{self._slash_if_needed()}\w+$",
                key,
            ):
                dirs.append(key.split("/")[-1])
        return dirs

    def pwd(self):
        """prints out the current path"""
        print(self.current_path)


fs = Filesystem()

with open(input_file, "r") as input:
    dirs = []
    files = []
    for line in input:
        line = line.strip()
        if line[0] == "$":
            if line[2:4] == "cd":
                # print(line[5 : len(line)])
                fs.cd(line[5 : len(line)])
            if line[2:4] == "ls":
                pass
        else:
            if line[0:3] == "dir":
                fs.write_dir(line[4 : len(line)])
            else:
                # print(line)
                file = line.split(" ")
                fs.write_file(file[1], int(file[0]))

answer1 = 0
for dir in fs.filesystem.keys():
    if fs.filesystem[dir]["__total_deep_size__"] <= 100000:
        answer1 += fs.filesystem[dir]["__total_deep_size__"]

write_output(output_file1, answer1)

required_space = 30000000
total_disk = 70000000
current_free_space = total_disk - fs.filesystem["/"]["__total_deep_size__"]
space_needed = required_space - current_free_space
print("We need", space_needed)

current_candidate = "/"
for dir in fs.filesystem.keys():
    if fs.filesystem[dir]["__total_deep_size__"] >= space_needed:
        # print(f'{fs.filesystem[dir]["__total_deep_size__"]} | {dir}')
        if (
            fs.filesystem[dir]["__total_deep_size__"]
            < fs.filesystem[current_candidate]["__total_deep_size__"]
        ):
            current_candidate = dir

print("delete this:", current_candidate)
write_output(output_file2, fs.filesystem[current_candidate]["__total_deep_size__"])
