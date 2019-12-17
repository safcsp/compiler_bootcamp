
class SymbolTable:
  def __init__(self, name, stype=None, parent=None):
    self.name = name
    self.stype = stype
    self.entriers = {}
    self.parent = parent
    self.children = []
    if parent != None:
      self.parent.children.append(self)
  
  def insert(self, name, entry):
    self.entriers[name] = entry
  
  def lookup(self, name):
    active_symt = self
    entry = None
    while active_symt != None:
      entry = active_symt.entriers.get(name, None)
      if entry != None:
        return entry
      active_symt = active_symt.parent


class SymtEntry:
  def __init__(self):
    pass

class VariableEntry:
  def __init__(self, datatype, location, value):
    self.datatype = datatype
    self.location = location
    self.value = value

class ParameterEntry:
  def __init__(self, datatype, location, default_value=None):
    self.datatype = datatype
    self.location = location
    self.default_value = default_value

class FunctionEntry:
  def __init__(self, datatype, parameters=[], symt=None):
    self.datatype = datatype
    self.parameters = parameters
    self.symt = symt

