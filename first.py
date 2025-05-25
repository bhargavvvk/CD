productions = [
    "X=TB","T=aB", "T=#", "B=b"
]

first_sets = {}

def find_first(symbol, productions, visited=None):
    if visited is None:
        visited = set()
    if symbol in visited:
        return set()
    if not symbol.isupper():
        return {symbol}

    visited.add(symbol)

    first_set = set()

    for prod in productions:
        if prod[0] == symbol:
            rhs = prod[2:]
            if rhs == '#':
                first_set.add('#')
            elif not rhs[0].isupper():
                first_set.add(rhs[0])
            else:
                first_of_first = find_first(rhs[0], productions, visited.copy())
                first_set.update(first_of_first - {'#'})

                if '#' in first_of_first and len(rhs) > 1:
                    for i in range(1, len(rhs)):
                        if not rhs[i].isupper():
                            first_set.add(rhs[i])
                            break
                        else:
                            next_first = find_first(rhs[i], productions, visited.copy())
                            first_set.update(next_first - {'#'})
                    else:
                        first_set.add('#')
    return first_set

nts = list(set(prod[0] for prod in productions))
for nt in nts:
    first_sets[nt] =  find_first(nt, productions)
for nt in first_sets:
    print(f"First({nt}) = {first_sets[nt]}")



                