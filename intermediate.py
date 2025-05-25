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
exp=infix_to_postfix("a+(b*c)+d")
print(exp)
def intermediate_code(exp):
  stack=[]
  temp_count=1
  for char in exp:
    if char in "+-*/":
      op2=stack.pop()
      op1=stack.pop()
      temp=f"t{temp_count}"
      print(f"{temp} = {op1} {char} {op2} ")
      stack.append(temp)
      temp_count+=1
    else:
      stack.append(char)
intermediate_code(exp)