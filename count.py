def count_file_contents(file_path):
    with open(file_path,'r') as file:
        content=file.read()
    nchar=len(content)
    nwords=len(content.split())
    nlines=content.count('\n')
    nspaces=content.count(' ')
    ntab=content.count('    ')
    print(f"characters :",nchar)
    print(f"characters :",nwords)
    print(f"characters :",nlines)
    print(f"characters :",nspaces)
    print(f"characters :",ntab)
count_file_contents('input.txt')