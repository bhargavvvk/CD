class Symbol_Table:
  def __init__(self):
    self.table={}
  def insert(self,name,type_,scope,value=None):
    if name in self.table:
      print(f"error")
    else:
      self.table[name]={
          'type':type_,
          'scope':scope,
          'value':value
      }
  def update(self,name,value):
    if name in self.table:
      self.table[name]['value']=value
    else:
      print("error")
  def lookup(self,name):
      if name in self.table:
        return self.table[name]
      else:
        print("not found")
        return None
  def delete(self,name):
    if name in self.table:
      del self.table[name]
    else:
      print("error")
  def display(self):
    print(f"\nSymbol_Table")
    print(f"name\ttype\tscope\tvalue")
    print("-"*30)
    for name,attributes in self.table.items():
      print(f"{name}\t{attributes['type']}\t{attributes['scope']}\t{attributes['value']}")
st=Symbol_Table()
st.insert("X","int","local")
st.insert("Y","int","local",10)
st.display()
st.delete("X")
st.update("Y",24)
st.display()