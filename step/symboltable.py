
class SymbolTable:
  def __init__(self, name):
    self.name = name
    self.entriers = {}
  
  def insert(self, name, entry):
    self.entriers[name] = entry
  
  def lookup(self, name):
    return self.entriers.get(name, None)

class SymtEntry:
  def __init__(self):
    pass

class VariableEntry:
  def __init__(self, datatype, location, value):
    self.datatype = datatype
    self.location = location
    self.value = value

