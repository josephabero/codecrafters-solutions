from enum import Enum
import sys

VERBOSE = False

def debug(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

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

    def is_at_end(self, index=None):
        index = self.current if index is None else index
        return index >= len(self.content)

    def peek(self):
        if self.is_at_end():
            return ""
        return self.content[self.current]

    def peek_next(self):
        if self.is_at_end(index=self.current + 1):
            return ""
        return self.content[self.current + 1]

    def advance(self):
        self.current += 1
        return self.content[self.current - 1]

    def read_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            # debug(f"Enter Scan: {self.current}")
            self.scan_token()
            # debug(f"Exit Scan: {self.current}")
        self.tokens.append(Token("EOF", "", "null", self.line))

        return self.tokens, self.errors

    def scan_token(self):
        token = self.advance()
        debug(f"Scanned: {token}")
        match token:
            # Brackets
            case "(": self.add_token("LEFT_PAREN")
            case ")": self.add_token("RIGHT_PAREN")
            case "{": self.add_token("LEFT_BRACE")
            case "}": self.add_token("RIGHT_BRACE")

            # Operators
            case "*": self.add_token("STAR")
            case "+": self.add_token("PLUS")
            case "-": self.add_token("MINUS")

            # Punctuation
            case ".": self.add_token("DOT")
            case ",": self.add_token("COMMA")
            case ";": self.add_token("SEMICOLON")

            # Longer Operators
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
            case "/":
                # Ignore Comment until Newline or EOF
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token("SLASH")

            # Ignore Whitespace
            case "\n":
                self.line += 1
            case "\t":
                return
            case "\r":
                return
            case " ":
                return

            # String
            case '"':
                lexical = ""
                while self.peek() != '"' and not self.is_at_end():
                    lexical += self.advance()

                if self.peek() == '"':
                    self.advance()
                    self.add_token("STRING", lexical=lexical)
                else:
                    self.add_error("Unterminated string.")

            case _:
                # Number
                if token.isnumeric():
                    lexical = self.number()
                    self.add_token("NUMBER", lexical=lexical)

                # Identifier
                elif token.isalpha() or token == "_":
                    self.identifier()
                    self.add_token("IDENTIFIER")

                # Default Error
                else:
                    debug(f"Adding error token for {self.current}: {token}")
                    self.add_error(f"Unexpected character: {token}")

    def add_token(self, type, lexical=None):
        text = self.content[self.start:self.current]
        self.tokens.append(Token(type, text, lexical, self.line))

    def add_error(self, error):
        self.errors.append(f"[line {self.line}] Error: {error}")

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.content[self.current] != expected:
            return False

        self.advance()
        return True

    def number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()

        while self.peek().isdigit():
            self.advance()

        return float(self.content[self.start:self.current])

    def identifier(self):
        while self.peek().isalpha() or \
              self.peek() == "_"    or \
              self.peek().isnumeric():
            self.advance()

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
