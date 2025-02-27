import shlex
import sys
import os

SHELL_HEADER = "$ "

ENV_PATH = os.getenv('PATH', "")
VERBOSE = int(os.getenv('VERBOSE', 0)) == 1

BUILTIN_COMMANDS = [
    "exit",
    "echo",
    "type",
    "pwd",
    "cd"
]

def log(message, *args):
    if VERBOSE:
        print(message, *args)

def find_in_path(param, paths=None, search_file=False, search_dir=False):
    # Get paths via PATH ENV variable
    if paths is None:
        paths = ENV_PATH.split(os.pathsep)

    # Check if param is a valid path
    if search_file and os.path.isfile(param):
        return param
    if search_dir and os.path.isdir(param):
        return param

    # Attempt Appended paths
    for path in paths:
        # Add forward slash if not included in path
        full_path = path
        if "/" != path[-1]:
            full_path += "/"
        full_path += param

        log(full_path, os.path.isfile(full_path))

        if search_file and os.path.isfile(full_path):
            return full_path
        if search_dir and os.path.isdir(full_path):
            return full_path

    # File not found in path
    return False


### Commands
def echo_command(args):
    print(*args)

def type_command(arg):
    if arg in BUILTIN_COMMANDS:
        print(f"{arg} is a shell builtin")
        return

    # Parse through paths
    path_found = find_in_path(arg, search_file=True)

    if path_found:
        print(f"{arg} is {path_found}")
    else:
        print(f"{arg}: not found")

def cd_command(arg):
    dir_found = find_in_path(arg, paths=[arg, os.getcwd()], search_dir=True)

    if arg == "~":
        os.chdir(os.path.expanduser("~"))
    elif arg == "..":
        os.chdir("..")
    elif dir_found:
        os.chdir(dir_found)
    else:
        print(f"cd: {arg}: No such file or directory")

def run_executable(command, shell_input):
    executable_found = find_in_path(command, search_file=True)

    if executable_found:
        log(f"Command '{executable_found}' found: Executing '{shell_input}'")
        os.system(shell_input)
        return True

    return False

def invalid_command(command):
    print(f"{command}: command not found")

def main():
    while True:
        # Print shell header
        sys.stdout.write(SHELL_HEADER)

        # Wait for user input
        shell_input = input()

        # Parse user input
        try:
            # print(shlex.split(shell_input, posix=True))
            command, *args = shlex.split(shell_input, posix=True)
        except:
            command = shell_input
            args = []

        log(command, args, *args)

        match command:
            case "exit":
                exit()

            case "echo":
                print(*args)

            case "type":
                type_command(*args)

            case "pwd":
                print(f"{os.getcwd()}")

            case "cd":
                cd_command(*args)

            case _:
                # Case: EXECUTABLE FILE
                executed = run_executable(command, shell_input)

                # Case: INVALID COMMAND
                if not executed:
                    invalid_command(command)


if __name__ == "__main__":
    main()
