# Python program to calculate First and Follow sets
def find_first(symbol, productions, first_sets, visited=None):
    if visited is None:
        visited = set()
    
    if symbol in visited:
        return set()
    # if symbol is not in visited, add it
    visited.add(symbol)
    
    if not symbol.isupper():  # Terminal
        return {symbol}
    
    first_set = set() # for our current symbol
    
    for prod in productions:
        if prod[0] == symbol:
            rhs = prod[2:]  # Right hand side after '='
            
            if rhs == '#':  # Epsilon production
                first_set.add('#')
            elif not rhs[0].isupper():  # First symbol is terminal
                first_set.add(rhs[0])
            else:  # First symbol is non-terminal
                first_of_first = find_first(rhs[0], productions, first_sets, visited.copy())
                first_set.update(first_of_first - {'#'})
                
                # Handle epsilon in first symbol
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
    
    return first_set

def find_follow(symbol, productions, first_sets, follow_sets, start_symbol):
    if symbol in follow_sets:
        return follow_sets[symbol]
    
    follow_set = set()
    
    # Add $ to start symbol
    if symbol == start_symbol:
        follow_set.add('$')
    
    for prod in productions:
        rhs = prod[2:]  # Right hand side
        for i, char in enumerate(rhs):
            if char == symbol:
                # If not last symbol
                while i + 1 < len(rhs):
                    next_symbol = rhs[i + 1]
                    if not next_symbol.isupper():  # Terminal
                        follow_set.add(next_symbol)
                        break
                    else:  # Non-terminal
                        first_of_next = first_sets.get(next_symbol, set())
                        follow_set.update(first_of_next - {'#'})
                        
                        # If epsilon in first of next symbol
                        if '#' not in first_of_next:
                            # Add follow of LHS
                            if prod[0] != symbol:  # Avoid infinite recursion
                                lhs_follow = find_follow(prod[0], productions, first_sets, follow_sets, start_symbol)
                                follow_set.update(lhs_follow)
                            break
                
                # If last symbol or all following symbols derive epsilon
                if i == len(rhs) - 1:
                    if prod[0] != symbol:  # Avoid infinite recursion
                        lhs_follow = find_follow(prod[0], productions, first_sets, follow_sets, start_symbol)
                        follow_set.update(lhs_follow)
    
    follow_sets[symbol] = follow_set
    return follow_set

def calculate_first_follow():
    # Grammar productions
    productions = [
    "X=TBCx","T=aB", "T=#", "B=b"
]
    
    # Get all non-terminals
    non_terminals = list(set(prod[0] for prod in productions))
    start_symbol = productions[0][0]
    
    # Calculate First sets
    first_sets = {}
    for nt in non_terminals:
        first_sets[nt] = find_first(nt, productions, first_sets)
    
    # Print First sets
    print("FIRST SETS:")
    print("-" * 30)
    for nt in sorted(non_terminals):
        first_list = sorted(list(first_sets[nt]))
        print(f"FIRST({nt}) = {{{', '.join(first_list)}}}")
    
    print("\nFOLLOW SETS:")
    print("-" * 30)
    
    # Calculate Follow sets
    follow_sets = {}
    for nt in sorted(non_terminals):
        follow_set = find_follow(nt, productions, first_sets, follow_sets, start_symbol)
        follow_list = sorted(list(follow_set))
        print(f"FOLLOW({nt}) = {{{', '.join(follow_list)}}}")

# Run the program
if __name__ == "__main__":
    calculate_first_follow()