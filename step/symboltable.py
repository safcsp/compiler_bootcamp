
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
    if self.is_exists(name):
      raise Exception("duplicated identifier " + name)
    self.entriers[name] = entry
  
  def is_exists(self, name):
    entry = self.entriers.get(name, None)
    return entry != None

  def lookup(self, name):
    active_symt = self
    entry = None
    while active_symt != None:
      entry = active_symt.entriers.get(name, None)
      if entry != None:
        return entry
      active_symt = active_symt.parent
  
  def type_lookup(self, stype):
    active_symt = self
    while active_symt != None:
      if active_symt.stype == stype:
        return active_symt
      active_symt = active_symt.parent
    
    return None


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

