# Tokenizer (Lexical Analysis)
def tokenize(expression):
    return [('a', 'a') if c == 'a' else ('b', 'b') for c in expression]

# Parser Class
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.derivation = []

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, token_type):
        if self.current_token() and self.current_token()[0] == token_type:
            self.pos += 1
            return True
        return False

    # Parse E -> A B (with branches for A and B on the same level)
    def parse_E(self, level=0):
        indent = " " * level  # Adjust indentation for better alignment
        if self.eat('a') and self.eat('b'):  # Try parsing E -> A B
            # First level: E branches into A and B with / and \ symbols
            self.derivation.append(f"{indent} E")
            self.derivation.append(f"{indent} / \\")  # Added '/' symbol from E to A
            self.derivation.append(f"{indent} A B")  # A and B on the same level
            # Second level: A derives 'a' and B derives 'b'
            self.derivation.append(f"{indent} | |")
            self.derivation.append(f"{indent} a b")  # Terminal a and b
            return True
        return False

    # Parse the input string and return the derivation path
    def parse(self):
        if self.parse_E() and self.pos == len(self.tokens):  # Check if entire string is consumed
            return '\n'.join(self.derivation)  # Return the derivation in vertical format
        else:
            return "Invalid input"

# Example usage
expression = "ab"  # or "a" or "b"
tokens = tokenize(expression)
parser = Parser(tokens)
derivation = parser.parse()
print(derivation)