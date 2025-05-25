import re

keywords={
    "int","while","for","return","if","else"
}

operators={
    "+","-","/","*","<=",">="
}

delimiters={
    ";",",","(",")","{","}"
}

def tokenize(line):
    return [t for t in re.split(r'(\s+|[;,\(\)\{\}])',line) if t.strip()]

def classify(token):
    if token in keywords: return "KEYWORDS"
    if token in operators: return "Operators"
    if token in delimiters: return "Delimiters"
    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$',token): return "Identifier"
    if re.match(r'\d+(\.\d+)?',token): return "NUMBER"
    else: return "UNKOWN"

def scanner(filepath):
    try:
        with open(filepath,'r') as f:
            content=f.read()
        for line in content.splitlines():
            for token in tokenize(line):
                print(token,classify(token))
    except Exception as e:
        print(e)
scanner("input.txt")
