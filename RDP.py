'''
Grammar:

E -> TE'
E' -> (+ | -)TE' | e
T -> FT'
T' -> (* | /)FT' | e
F -> ( E ) | digit
'''

class Parser:
    def __init__(self, string):
        self.input = string.replace(" ","")
        self.pos = 0
    def current_token(self):
        return self.input[self.pos] if self.pos < len(self.input) else None
    def match(self, expected):
        if self.current_token() == expected:
            self.pos += 1
            return True
        return False
    def number(self):
        start = self.pos
        while self.current_token() and self.current_token().isdigit():
            self.pos+=1
        return start!=self.pos
    def F(self):
        if self.match('('):
            if self.E() and self.match(')'):
                return True
            return False
        return self.number()
    def Tprime(self):
        if self.match('*') or self.match('/'):
            if self.F():
                return self.Tprime()
            return False
        return True
    def T(self):
        if self.F():
            return self.Tprime()
        return False
    def Eprime(self):
        if self.match("+") or self.match("-"):
            if self.E():
                return self.Eprime()
            return False
        return True
    def E(self):
        if self.T():
            return self.Eprime()
        return False
    def parse(self):
        return self.E() and self.pos == len(self.input)

examples = [
    '1+2+3',
    '(1+2)*3',
    "1+*3",
    '(((1)))'
]

for string in examples:
    parser = Parser(string)
    print(f"{string:<10}",parser.parse())
