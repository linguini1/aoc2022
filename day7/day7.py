# Advent of Code: Day 7
__author__ = "Matteo Golin"

# Imports

# Constants
INPUT_FILE = "./input.txt"
MAX_SIZE = 100_000
DISK_SPACE = 70000000
REQ_UNUSED_SPACE = 30000000

# Types
DirectoryList = list[str]
File = tuple[int, str]
FileList = list[File]
FileStructure = dict[str, list[DirectoryList, FileList]]


# Main
def create_file_structure(terminal_output: list[str]) -> FileStructure:

    """Returns a dictionary representation of the file structure determined by the terminal output."""

    file_structure: dict[str, tuple[DirectoryList, FileList]] = {}
    current_dir = []
    record_files: bool = False
    for line in terminal_output:

        # Detect command
        if "$" in line:

            record_files = False  # Every time a new command is processed, finish recording previous ls
            command = line.split(" ")[1:]  # Ignore $ symbol

            # Process directory change (cd command)
            if "cd" in command:
                directory = command[-1]

                if directory == "..":  # Move up
                    current_dir.pop()
                else:
                    current_dir.append(directory)  # Move into directory

                    # Directory has not been seen before
                    cur_dir_str = "/".join(current_dir)
                    if not file_structure.get(cur_dir_str):
                        file_structure[cur_dir_str] = [[], []]

            # ls command
            else:
                record_files = True

        # Terminal response, only ever to ls
        # If recording, then store all the files and directories in the current dir key
        elif record_files:
            info = line.split(" ")
            cur_dir_str = "/".join(current_dir)

            # Record directory
            if "dir" in info:
                file_structure[cur_dir_str][0].append(f"{cur_dir_str}/{info[1]}")

            # Record file
            else:
                size, name = info
                file: File = (int(size), name)
                file_structure[cur_dir_str][1].append(file)

    return file_structure


def sum_file_sizes(file_structure: FileStructure, directory: str) -> int:

    """Returns the total size of all the files in the directory."""

    return sum([f[0] for f in file_structure[directory][1]])


def get_directory_sizes(f_struct: FileStructure, root: str, sizes: dict) -> int:

    """Returns a dictionary with directories associated with their total size."""

    children = f_struct[root][0]
    file_total = sum_file_sizes(f_struct, root)

    if not children:
        sizes[root] = file_total
    else:
        sizes[root] = file_total + sum([get_directory_sizes(f_struct, child, sizes) for child in children])

    return sizes[root]


def main():

    # Unpack input
    with open(INPUT_FILE, 'r') as file:
        raw_data: list[str] = file.read().split("\n")[:-1]

    # Create file structure
    file_structure = create_file_structure(raw_data)

    # Part 1
    # What is the sum of the total size of the directories with a size greater than 100,000
    dir_sizes = {}
    get_directory_sizes(file_structure, "/", dir_sizes)

    total_sizes = 0
    for _, size in dir_sizes.items():
        if size <= MAX_SIZE:
            total_sizes += size

    print(f"The total size of the directories with a size over 100,000 is {total_sizes}.")

    # Part 2
    # What is the smallest directory that can be deleted to free up enough space to update
    options = []  # What directories are big enough to be considered
    used_space = dir_sizes["/"]
    free_space = DISK_SPACE - used_space

    for directory, size in dir_sizes.items():
        if size >= REQ_UNUSED_SPACE - free_space:
            options.append((directory, size))

    # What is the smallest directory that can be chosen
    smallest = min(options, key=lambda x: x[1])
    print(f"The smallest directory that can be deleted is {smallest[0]} with a size of {smallest[1]} ")


if __name__ == '__main__':
    main()
