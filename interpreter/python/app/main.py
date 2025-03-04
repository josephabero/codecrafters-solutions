from scanner import Scanner
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh <command> <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    match command:
        case "tokenize":
            tokenize(filename)
        case _:
            print(f"Unknown command: {command}", file=sys.stderr)
            exit(1)

def tokenize(filename):
    with open(filename) as file:
        file_contents = file.read()

    scanner = Scanner(file_contents)

    tokens, errors = scanner.read_tokens()

    for error in errors:
        print(error, file=sys.stderr)

    for token in tokens:
        print(token)

    if errors:
        exit(65)
    else:
        exit(0)


if __name__ == "__main__":
    main()
