def find_first(symbol, productions, first_sets, visited=None):
    if visited is None:
        visited = set()

    if symbol in visited:
        return set()
    visited.add(symbol)

    if not symbol.isupper():  # Terminal
        return {symbol}

    first_set = set()

    for prod in productions:
        if prod[0] == symbol:
            rhs = prod[2:]

            if rhs == '#':  # Epsilon production
                first_set.add('#')
            elif not rhs[0].isupper():
                first_set.add(rhs[0])
            else:
                first_of_first = find_first(rhs[0], productions, first_sets, visited.copy())
                first_set.update(first_of_first)

                if '#' in first_of_first and len(rhs) > 1:
                    for i in range(1, len(rhs)):
                        if not rhs[i].isupper():
                            first_set.add(rhs[i])
                            break
                        else:
                            next_first = find_first(rhs[i], productions, first_sets, visited.copy())
                            first_set.update(next_first - {'#'})
                            if '#' not in next_first:
                                break
                    else:
                        first_set.add('#')
# hello
    return first_set

def find_follow(symbol, productions, first_sets, follow_sets, start_symbol):
    if symbol in follow_sets:
        return follow_sets[symbol]

    follow_set = set()
    if symbol == start_symbol:
        follow_set.add('$')

    for prod in productions:
        lhs = prod[0]
        rhs = prod[2:]
        for i, char in enumerate(rhs):
            if char == symbol:
                if i + 1 < len(rhs):
                    next_symbol = rhs[i + 1]
                    if not next_symbol.isupper():
                        follow_set.add(next_symbol)
                    else:
                        first_of_next = first_sets.get(next_symbol, set())
                        follow_set.update(first_of_next - {'#'})
                        if '#' in first_of_next:
                            if lhs != symbol:
                                lhs_follow = find_follow(lhs, productions, first_sets, follow_sets, start_symbol)
                                follow_set.update(lhs_follow)
                else:
                    if lhs != symbol:
                        lhs_follow = find_follow(lhs, productions, first_sets, follow_sets, start_symbol)
                        follow_set.update(lhs_follow)

    follow_sets[symbol] = follow_set
    return follow_set

def construct_parsing_table(productions, first_sets, follow_sets):
    table = {}
    for prod in productions:
        lhs = prod[0]
        rhs = prod[2:]

        table.setdefault(lhs, {})

        first_rhs = set()
        if rhs == '#':
            first_rhs.add('#')
        else:
            for i in range(len(rhs)):
                if not rhs[i].isupper():
                    first_rhs.add(rhs[i])
                    break
                sub_first = first_sets[rhs[i]]
                first_rhs.update(sub_first - {'#'})
                if '#' not in sub_first:
                    break
            else:
                first_rhs.add('#')

        for terminal in first_rhs - {'#'}:
            table[lhs][terminal] = rhs
        if '#' in first_rhs:
            for terminal in follow_sets[lhs]:
                table[lhs][terminal] = '#'

    return table

def print_parsing_table(table):
    print("\nLL(1) PARSING TABLE:")
    print("-" * 50)
    for nt in sorted(table):
        for terminal in sorted(table[nt]):
            print(f"M[{nt}][{terminal}] = {nt} → {table[nt][terminal]}")

def parse_input(input_string, start_symbol, parsing_table):
    stack = ['$']
    stack.append(start_symbol)
    input_string += '$'
    index = 0

    print("\nParsing steps:")
    while stack:
        top = stack[-1]
        current_input = input_string[index]
        print(f"Stack: {stack} | Input: {input_string[index:]}")

        if top == current_input:
            stack.pop()
            index += 1
        elif not top.isupper():
            print("Error: Terminal mismatch")
            return
        elif current_input in parsing_table.get(top, {}):
            stack.pop()
            production = parsing_table[top][current_input]
            if production != '#':
                stack.extend(reversed(production))
        else:
            print("Error: No rule for this input")
            return

    if index == len(input_string):
        print("✅ String accepted!")
    else:
        print("❌ String rejected!")

def calculate_first_follow():
    productions = [
        "X=TnS", "X=Rm", "T=q", "T=#", 
        "S=p", "S=#", "R=om", "R=ST"
    ]

    non_terminals = list(set(prod[0] for prod in productions))
    start_symbol = productions[0][0]

    first_sets = {}
    for nt in non_terminals:
        first_sets[nt] = find_first(nt, productions, first_sets)

    print("FIRST SETS:")
    print("-" * 30)
    for nt in sorted(non_terminals):
        first_list = sorted(list(first_sets[nt]))
        print(f"FIRST({nt}) = {{{', '.join(first_list)}}}")

    follow_sets = {}
    print("\nFOLLOW SETS:")
    print("-" * 30)
    for nt in sorted(non_terminals):
        follow_set = find_follow(nt, productions, first_sets, follow_sets, start_symbol)
        follow_list = sorted(list(follow_set))
        print(f"FOLLOW({nt}) = {{{', '.join(follow_list)}}}")

    parsing_table = construct_parsing_table(productions, first_sets, follow_sets)
    print_parsing_table(parsing_table)

    # Try parsing a string
    input_str = input("\nEnter input string to parse: ")
    parse_input(input_str, start_symbol, parsing_table)

if __name__ == "__main__":
    calculate_first_follow()
