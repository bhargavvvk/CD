# Complete SLR Parser Implementation
from collections import defaultdict

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
                found_terminal = False
                for j in range(i + 1, len(rhs)):
                    next_symbol = rhs[j]
                    if not next_symbol.isupper():  # Terminal
                        follow_set.add(next_symbol)
                        found_terminal = True
                        break
                    else:  # Non-terminal
                        first_of_next = first_sets.get(next_symbol, set())
                        follow_set.update(first_of_next - {'#'})
                        
                        # If epsilon not in first of next symbol
                        if '#' not in first_of_next:
                            found_terminal = True
                            break
                
                # If last symbol or all following symbols derive epsilon
                if not found_terminal:
                    if prod[0] != symbol:  # Avoid infinite recursion
                        lhs_follow = find_follow(prod[0], productions, first_sets, follow_sets, start_symbol)
                        follow_set.update(lhs_follow)
    
    follow_sets[symbol] = follow_set
    return follow_set

class LRItem:
    def __init__(self, lhs, rhs, dot_pos, rule_num):
        self.lhs = lhs
        self.rhs = rhs
        self.dot_pos = dot_pos
        self.rule_num = rule_num
    
    def __eq__(self, other):
        return (self.lhs == other.lhs and 
                self.rhs == other.rhs and 
                self.dot_pos == other.dot_pos)
    
    def __hash__(self):
        return hash((self.lhs, tuple(self.rhs), self.dot_pos))
    
    def __str__(self):
        rhs_with_dot = self.rhs[:self.dot_pos] + ['.'] + self.rhs[self.dot_pos:]
        return f"{self.lhs} -> {' '.join(rhs_with_dot)}"
    
    def next_symbol(self):
        if self.dot_pos < len(self.rhs):
            return self.rhs[self.dot_pos]
        return None
    
    def is_complete(self):
        return self.dot_pos >= len(self.rhs)

class SLRParser:
    def __init__(self):
        self.productions = []
        self.terminals = set()
        self.non_terminals = set()
        self.first_sets = {}
        self.follow_sets = {}
        self.start_symbol = None
        self.states = []
        self.goto_table = {}
        self.action_table = {}
        
    def parse_productions(self, prod_strings):
        """Parse production strings into structured format"""
        self.productions = []
        rule_num = 0
        
        for prod_str in prod_strings:
            lhs, rhs = prod_str.split('=')
            if rhs == '#':
                rhs_symbols = []
            else:
                rhs_symbols = list(rhs)
            
            self.productions.append((lhs, rhs_symbols, rule_num))
            self.non_terminals.add(lhs)
            
            for symbol in rhs_symbols:
                if symbol.isupper():
                    self.non_terminals.add(symbol)
                else:
                    self.terminals.add(symbol)
            
            rule_num += 1
        
        # Add augmented start production
        if self.productions:
            original_start = self.productions[0][0]
            self.start_symbol = original_start + "'"
            self.productions.insert(0, (self.start_symbol, [original_start], rule_num))
            self.non_terminals.add(self.start_symbol)
        
        self.terminals.add('$')  # End of input marker
    
    def closure(self, items):
        """Compute closure of a set of LR(0) items"""
        closure_items = set(items)
        changed = True
        
        while changed:
            changed = False
            new_items = set()
            
            for item in closure_items:
                next_sym = item.next_symbol()
                if next_sym and next_sym.isupper():  # Non-terminal
                    # Add all productions for this non-terminal
                    for lhs, rhs, rule_num in self.productions:
                        if lhs == next_sym:
                            new_item = LRItem(lhs, rhs, 0, rule_num)
                            if new_item not in closure_items:
                                new_items.add(new_item)
                                changed = True
            
            closure_items.update(new_items)
        
        return closure_items
    
    def goto(self, items, symbol):
        """Compute GOTO(items, symbol)"""
        goto_items = set()
        
        for item in items:
            if item.next_symbol() == symbol:
                new_item = LRItem(item.lhs, item.rhs, item.dot_pos + 1, item.rule_num)
                goto_items.add(new_item)
        
        return self.closure(goto_items)
    
    def build_lr0_automaton(self):
        """Build LR(0) automaton (set of states)"""
        # Initial state
        start_item = LRItem(self.start_symbol, [self.productions[0][1][0]], 0, 0)
        initial_state = self.closure({start_item})
        
        self.states = [initial_state]
        self.goto_table = {}
        
        # Build all states
        i = 0
        while i < len(self.states):
            current_state = self.states[i]
            
            # Find all symbols that can be shifted from this state
            symbols = set()
            for item in current_state:
                next_sym = item.next_symbol()
                if next_sym:
                    symbols.add(next_sym)
            
            # For each symbol, compute GOTO and add new states if necessary
            for symbol in symbols:
                new_state = self.goto(current_state, symbol)
                if new_state:
                    # Check if this state already exists
                    state_index = None
                    for j, existing_state in enumerate(self.states):
                        if new_state == existing_state:
                            state_index = j
                            break
                    
                    if state_index is None:
                        state_index = len(self.states)
                        self.states.append(new_state)
                    
                    self.goto_table[(i, symbol)] = state_index
            
            i += 1
    
    def build_parsing_table(self):
        """Build SLR parsing table"""
        self.action_table = {}
        
        for i, state in enumerate(self.states):
            for item in state:
                if item.is_complete():
                    if item.lhs == self.start_symbol:
                        # Accept action
                        self.action_table[(i, '$')] = ('accept', None)
                    else:
                        # Reduce action
                        follow_symbols = self.follow_sets.get(item.lhs, set())
                        for symbol in follow_symbols:
                            if (i, symbol) in self.action_table:
                                print(f"Conflict at state {i}, symbol {symbol}")
                            self.action_table[(i, symbol)] = ('reduce', item.rule_num)
                else:
                    # Shift action
                    next_sym = item.next_symbol()
                    if next_sym and not next_sym.isupper():  # Terminal
                        if (i, next_sym) in self.goto_table:
                            next_state = self.goto_table[(i, next_sym)]
                            if (i, next_sym) in self.action_table:
                                print(f"Conflict at state {i}, symbol {next_sym}")
                            self.action_table[(i, next_sym)] = ('shift', next_state)
    
    def print_states(self):
        """Print all LR(0) states"""
        pass  # State construction output removed
    
    def print_parsing_table(self):
        """Print the SLR parsing table"""
        print("\nSLR PARSING TABLE:")
        print("=" * 80)
        
        # Header
        terminals = sorted(self.terminals)
        non_terminals = sorted(self.non_terminals - {self.start_symbol})
        
        print(f"{'State':<8}", end='')
        for t in terminals:
            print(f"{t:<10}", end='')
        print(f"{'|':<3}", end='')
        for nt in non_terminals:
            print(f"{nt:<8}", end='')
        print()
        
        print("-" * 80)
        
        for i in range(len(self.states)):
            print(f"{i:<8}", end='')
            
            # Action part
            for t in terminals:
                if (i, t) in self.action_table:
                    action, param = self.action_table[(i, t)]
                    if action == 'shift':
                        print(f"s{param:<9}", end='')
                    elif action == 'reduce':
                        print(f"r{param:<9}", end='')
                    elif action == 'accept':
                        print(f"{'acc':<10}", end='')
                else:
                    print(f"{'':<10}", end='')
            
            print(f"{'|':<3}", end='')
            
            # Goto part
            for nt in non_terminals:
                if (i, nt) in self.goto_table:
                    print(f"{self.goto_table[(i, nt)]:<8}", end='')
                else:
                    print(f"{'':<8}", end='')
            print()
    
    def parse_input(self, input_string):
        """Parse input string using the SLR parser"""
        print(f"\nPARSING INPUT: {input_string}")
        print("=" * 50)
        
        # Initialize
        stack = [0]  # State stack
        input_buffer = list(input_string) + ['$']
        input_ptr = 0
        step = 1
        
        print(f"{'Step':<6}{'Stack':<20}{'Input':<15}{'Action':<20}")
        print("-" * 60)
        
        while True:
            current_state = stack[-1]
            current_symbol = input_buffer[input_ptr]
            
            # Print current configuration
            stack_str = ' '.join(map(str, stack))
            input_str = ''.join(input_buffer[input_ptr:])
            
            if (current_state, current_symbol) not in self.action_table:
                print(f"{step:<6}{stack_str:<20}{input_str:<15}ERROR: No action")
                return False
            
            action, param = self.action_table[(current_state, current_symbol)]
            
            if action == 'shift':
                print(f"{step:<6}{stack_str:<20}{input_str:<15}Shift {param}")
                stack.append(param)
                input_ptr += 1
                
            elif action == 'reduce':
                # Find the production to reduce by
                production = None
                for lhs, rhs, rule_num in self.productions:
                    if rule_num == param:
                        production = (lhs, rhs)
                        break
                
                if production:
                    lhs, rhs = production
                    print(f"{step:<6}{stack_str:<20}{input_str:<15}Reduce by {lhs} -> {''.join(rhs) if rhs else '#'}")
                    
                    # Pop states equal to length of RHS
                    for _ in range(len(rhs)):
                        if len(stack) > 1:
                            stack.pop()
                    
                    # Push GOTO state
                    if (stack[-1], lhs) in self.goto_table:
                        stack.append(self.goto_table[(stack[-1], lhs)])
                    else:
                        print(f"ERROR: No GOTO({stack[-1]}, {lhs})")
                        return False
                
            elif action == 'accept':
                print(f"{step:<6}{stack_str:<20}{input_str:<15}ACCEPT")
                print(f"\nInput '{input_string}' is ACCEPTED!")
                return True
            
            step += 1
            
            # Prevent infinite loops
            if step > 100:
                print("ERROR: Too many steps, possible infinite loop")
                return False
        
        return False

def main():
    parser = SLRParser()
    
    # Get grammar from user
    print("Enter grammar productions (one per line, format: A=BC or A=#)")
    print("Enter 'done' when finished:")
    
    productions = []
    while True:
        prod = input().strip()
        if prod.lower() == 'done':
            break
        if prod:
            productions.append(prod)
    
    if not productions:
        # Use default grammar for testing
        productions = ["S=AB", "A=a", "A=#", "B=b"]
        print(f"Using default grammar: {productions}")
    
    # Parse productions
    parser.parse_productions(productions)
    
    # Convert productions for FIRST/FOLLOW calculation
    converted_prods = []
    for lhs, rhs, _ in parser.productions[1:]:  # Skip augmented production
        if not rhs:
            converted_prods.append(f"{lhs}=#")
        else:
            converted_prods.append(f"{lhs}={''.join(rhs)}")
    
    # Calculate FIRST sets
    for nt in parser.non_terminals:
        if nt != parser.start_symbol:
            parser.first_sets[nt] = find_first(nt, converted_prods, parser.first_sets)
    
    # Calculate FOLLOW sets
    original_start = parser.productions[1][0]  # Original start symbol
    for nt in parser.non_terminals:
        if nt != parser.start_symbol:
            parser.follow_sets[nt] = find_follow(nt, converted_prods, parser.first_sets, parser.follow_sets, original_start)
    
    print("\nFIRST SETS:")
    for nt in sorted(parser.non_terminals - {parser.start_symbol}):
        print(f"FIRST({nt}) = {parser.first_sets.get(nt, set())}")
    
    print("\nFOLLOW SETS:")
    for nt in sorted(parser.non_terminals - {parser.start_symbol}):
        print(f"FOLLOW({nt}) = {parser.follow_sets.get(nt, set())}")
    
    # Build LR(0) automaton
    parser.build_lr0_automaton()
    # State construction output removed
    
    # Build parsing table
    parser.build_parsing_table()
    parser.print_parsing_table()
    
    # Parse input strings
    while True:
        input_str = input("\nEnter string to parse (or 'quit' to exit): ").strip()
        if input_str.lower() == 'quit':
            break
        if input_str:
            parser.parse_input(input_str)

if __name__ == "__main__":
    main()