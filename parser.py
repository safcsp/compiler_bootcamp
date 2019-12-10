from tokenizer import *

class Node:
  pass

class Statement(Node):
  pass

class BlockStatement(Node):
  pass

class VarStatement(Statement):
  def __init__(self, token, datatype, identifier, value):
    self.token = token
    self.datatype = datatype
    self.identifer = identifier
    self.value = value

class Parser:
  def __init__(self, tokenizer):
    self.tokenizer = tokenizer
    self.current_token = None
  
  def syntax_error(self, token, message):
    raise Exception('[Step(syntax error)]:' + message + ', ' + token.value + ', line number: ' + str(token.line_number) + ', position: ' + str(token.position))

  def var_parser(self):
    # var datatype id = literal
    var_token = self.current_token
    self.current_token = self.tokenizer.tokenize()

    if not self.current_token.category == 'keyword' and not self.current_token.value in ['int', 'float', 'string', 'boolean']:
      self.syntax_error(self.current_token, 'datatype expected')

    datatype_token = self.current_token

    self.current_token = self.tokenizer.tokenize()
    if self.current_token.category != 'identifier':
      self.syntax_error(self.current_token, 'identifier expected')

    identifier_token = self.current_token
    self.current_token = self.tokenizer.tokenize()
    if not self.current_token.value == '=':
      self.syntax_error(self.current_token,'assignment operator expected')

    self.current_token = self.tokenizer.tokenize()
    if self.current_token.category != 'literal':
      self.syntax_error(self.current_token,'literal expected')

    literal_token = self.current_token

    return VarStatement(var_token, datatype_token, identifier_token, literal_token)

  def parse(self):
    self.current_token = self.tokenizer.tokenize()
    if self.current_token.value == 'eof':
      return None

    if self.current_token.category == 'keyword':
      if self.current_token.value == 'var':
        return self.var_parser()
    elif self.current_token.category == 'comment':
      return None
    elif self.current_token.category == 'whitespace':
      return None
    elif self.current_token.category == 'error':
      self.syntax_error(self.current_token, 'unexpected token')
    else:
      self.syntax_error(self.current_token, 'unexpected token')
    
    return None