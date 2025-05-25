def target_code(three_address):
  for line in three_address:
    lhs,rhs=line.split('=')
    lhs=lhs.strip()
    rhs=rhs.strip()
    tokens=rhs.split()
    if len(tokens)==3:
      op=tokens[1]
      if op=='+':
        instruction="ADD"
      elif op=='-':
        instruction="SUB"
      elif op=='*':
        instruction="MUL"
      elif op=='/':
        instruction="DIV"
      else:
        instruction="UNKOWN"
      print(f"MOV R1 {tokens[0]}")
      print(f"{instruction} R1 {tokens[2]}")
      print(f"MOV {lhs} R1")
    else:
      print(f"MOV {lhs} {rhs}")
three_address=['t1 = b * c','t2 = a + t1 ','t3 = t2 + d ']
target_code(three_address)