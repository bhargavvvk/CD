def code_optimization(code):
    optimized = []
    for line in code:
        lhs, rhs = line.split(' = ')
        try:
            result = eval(rhs)
            optimized.append(f"{lhs} = {result}")
        except:
            optimized.append(line)
    print("\n5. Code Optimization:")
    for line in optimized:
        print(" ", line)
    return optimized
def constant_propagation(code):
    constants = {}
    optimized = []
    for line in code:
        if '=' in line:
            var, expr = line.split('=')
            var, expr = var.strip(), expr.strip()
            for c in constants:
                expr = expr.replace(c, str(constants[c]))
            try:
                result = eval(expr)
                constants[var] = result
                optimized.append(f"{var} = {result}")
            except:
                constants[var] = expr
                optimized.append(f"{var} = {expr}")
        else:
            optimized.append(line)
    return optimized
code=["a = 5", "b = a + 3"]
print(constant_propagation(code))

import re

def common_subexpression_elimination(code):
    expr_table = {}
    optimized_code = []

    for line in code:
        var, expr = line.split('=')

        if expr in expr_table:
            old_var = expr_table[expr]
            optimized_code.append(f"{var} = {old_var}")
        else:
            expr_table[expr] = var
            optimized_code.append(line)

    return optimized_code

code1 = [
    "t1 = a + b",
    "t2 = a + b",
    "t3 = c + d",
    "t4 = a + b",
    "t5 = t1 + t3"
]

optimized = common_subexpression_elimination(code1)

for line in optimized:
    print(line)

def dead_code_elimination(code):
    lines = code.split("\n")
    used_vars = set()
    result = []
    for line in lines[::-1]:
        if "=" in line:
            var, expr = line.split("=")
            if var.strip() in used_vars or not used_vars:
                used_vars.update(expr.strip().split())
                result.append(line)
        else:
            used_vars.update(line.strip().split())
            result.append(line)
    return "\n".join(result[::-1])

print(dead_code_elimination("a = c\nd = c * b + 6\ns = a * b"))

def strength_reduction(expr):
    return expr.replace("* 2", "+ x").replace("x * 2", "x + x").replace("x**2", "x * x")
def loop_invariant_code_motion(code_lines):
    invariant = []
    loop_body = []
    inside_loop = False

    for line in code_lines:
        line = line.strip()
        if line.startswith("for") or line.startswith("while"):
            inside_loop = True
            loop_body.append(line)
        elif inside_loop:
            if any(var in line for var in ['i', 'j', 'k']):  # crude check
                loop_body.append(line)
            else:
                invariant.append(line)
        else:
            invariant.append(line)

    print("--- Optimized Code ---")
    for line in invariant:
        print(line)
    for line in loop_body:
        print(line)

# Example
input_code = [
    "for i in range(0, n):",
    "    x = a + b",
    "    arr[i] = x * i"
]

loop_invariant_code_motion(input_code)