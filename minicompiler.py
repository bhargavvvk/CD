import re

code="x=5+3*2"

def lexical_analyzer(code):
  tokens=re.findall(r'[a-zA-Z_]\w*|==|<=|>=|!=|[0-9]+|[+\-*/=()]',code)
  print(f"1.Lexical Analyzer",tokens)
  return tokens

x=lexical_analyzer(code)
def syntax_analysis(tokens):
  if tokens[1]!='=':
    SyntaxError("Expected = after identifier")
  print("2. Syntax Analysis(parse tree)")
  print("assignment")
  print("  |--identifier",tokens[0])
  print("  |--expression",' '.join(tokens[2:]))
  return ("assign",tokens[0],tokens[2:])
y=syntax_analysis(x)

def semantic_analsis(ast):
  _,var,exp=ast
  for token in exp:
    if(re.match(r'[a-zA-Z_]\w*',token) and var!=token):
      raise NameError(f"Undeclared Variable: {token}")
  print(f"3. semantic analysis: PASSED")
  return True
z=semantic_analsis(y)
def infix_to_postfix(tokens):
  precedence={'+':1,'-':1,'*':2,'/':2}
  output,stack=[],[]
  for token in tokens:
    if token.isnumeric() or token.isalpha():
      output.append(token)
    elif token=='(':
      stack.append(token)
    elif token==')':
      while stack and stack[-1]!='(':
        output.append(stack.pop())
      stack.pop()
    elif token in precedence:
      while stack and stack[-1]!='(' and precedence.get(stack[-1],0)>=precedence.get(token):
        output.append(stack.pop())
      stack.append(token)
  while stack:
    output.append(stack.pop())
  return output
def three_address_code(exp):
  stack=[]
  code=[]
  temp_count=1
  for char in exp:
    if char in "+-*/":
      op2=stack.pop()
      op1=stack.pop()
      temp=f"t{temp_count}"
      code.append(f"{temp} = {op1} {char} {op2} ")
      stack.append(temp)
      temp_count+=1
    else:
      stack.append(char)
  return code,stack
three_address_code(exp)
def intermediate_code(ast):
  _,var,exp=ast
  postfix=infix_to_postfix(exp)
  code,stack=three_address_code(postfix)
  code.append(f"{var} ={stack[0]}")
  print(f"4. Intermediate Code : Three Address Format")
  for line in code:
    print(" ",line)
  return code
intermediate = intermediate_code(y)

def code_optimization(intermediate):
  optimized=[]
  for line in intermediate:
    parts=line.split("=")
    if len(parts)==2:
      dest,expr=parts
      try:
        result=eval(expr)
        optimized.append(f"{dest} = {result}")
      except:
        optimized.append(line)
  print(f"5. optimized code")
  for line in optimized:
    print(" ",line)
  return optimized

optimized_code=code_optimization(intermediate)
def generate_assembly(optimized_code):
    print("\n6. Code Optimization:")
    for line in optimized_code:
        lhs, rhs = line.split('=')
        lhs = lhs.strip()
        rhs = rhs.strip()
        tokens = rhs.split()
        if len(tokens) == 3:
            op = tokens[1]
            if op == '+':
                instruction = "ADD"
            elif op == '-':
                instruction = "SUB"
            elif op == '*':
                instruction = "MUL"
            elif op == '/':
                instruction = "DIV"
            else:
                instruction = "UNKNOWN"

            print(f"MOV R1, {tokens[0]}")
            print(f"{instruction} R1, {tokens[2]}")
            print(f"MOV {lhs}, R1")
        else:
            print(f"MOV {lhs}, {rhs}")
generate_assembly(optimized_code)