from enum import Enum
import sys

class Token():
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        literal = "null" if self.literal is None else self.literal
        return f"{self.type} {self.lexeme} {literal}"

class Scanner():
    def __init__(self, content):
        self.content = content
        self.errors = []
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def is_at_end(self):
        return self.current >= len(self.content)

    def advance(self):
        self.current += 1
        return self.content[self.current - 1]

    def read_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token("EOF", "", "null", self.line))

        return self.tokens, self.errors

    def scan_token(self):
        token = self.advance()
        match token:
            case "(": self.add_token("LEFT_PAREN")
            case ")": self.add_token("RIGHT_PAREN")
            case "{": self.add_token("LEFT_BRACE")
            case "}": self.add_token("RIGHT_BRACE")
            case "*": self.add_token("STAR")
            case ".": self.add_token("DOT")
            case ",": self.add_token("COMMA")
            case "+": self.add_token("PLUS")
            case "-": self.add_token("MINUS")
            case ";": self.add_token("SEMICOLON")
            case "!":
                token_to_add = "BANG_EQUAL" if self.match("=") else "BANG"
                self.add_token(token_to_add)
            case "=":
                token_to_add = "EQUAL_EQUAL" if self.match("=") else "EQUAL"
                self.add_token(token_to_add)
            case "<":
                token_to_add = "LESS_EQUAL" if self.match("=") else "LESS"
                self.add_token(token_to_add)
            case ">":
                token_to_add = "GREATER_EQUAL" if self.match("=") else "GREATER"
                self.add_token(token_to_add)
            case _:   self.add_error(token)

    def add_token(self, type, lexical=None):
        text = self.content[self.start:self.current]
        self.tokens.append(Token(type, text, lexical, self.line))

    def add_error(self, token):
        self.errors.append(f"[line {self.line}] Error: Unexpected character: {token}")

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.content[self.current] != expected:
            return False

        self.advance()
        return True

def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

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
