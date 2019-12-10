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

class PrintStatement(Statement):
  def __init__(self, token, literal):
    self.token = token
    self.literal = literal

class WhileStatement(BlockStatement):
  def __init__(self, token, literal, statements=[]):
    self.token = token
    self.literal = literal
    self.statements = statements

class Parser:
  def __init__(self, tokenizer):
    self.tokenizer = tokenizer
    self.current_token = None
    self.current_level = 0
  
  def syntax_error(self, token, message):
    raise Exception('[Step(syntax error)]:' + message + ', ' + token.value + ', line number: ' + str(token.line_number) + ', position: ' + str(token.position))

  def print_parser(self):
    # print literal
    print_token = self.current_token
    self.current_token = self.tokenizer.tokenize()
    if self.current_token.category != 'literal':
      self.syntax_error(self.current_token, 'literal expected')
    
    return PrintStatement(print_token, self.current_token)

  def match(self, token_value):
    self.current_token = self.tokenizer.tokenize()
    if self.current_token.value != token_value:
      self.syntax_error(self.current_token, 'unexpected token')
    
  def while_parser(self):
    # while literal {statements} 
    while_token = self.current_token
    self.current_token = self.tokenizer.tokenize()

    if self.current_token.category != 'literal':
      self.syntax_error(self.current_token, 'literal expected')
    
    literal_token = self.current_token

    self.match('{')
    self.current_level += 1
    statements = self.parse()
    #self.match('}')

    return WhileStatement(while_token, literal_token, statements)

    
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
    self.match('=')

    self.current_token = self.tokenizer.tokenize()
    if self.current_token.category != 'literal':
      self.syntax_error(self.current_token,'literal expected')

    literal_token = self.current_token

    return VarStatement(var_token, datatype_token, identifier_token, literal_token)

  def parse(self):
    statements = []
    self.current_token = self.tokenizer.tokenize()

    while self.current_token.category != 'EOF':

      if self.current_token.category == 'keyword':
        if self.current_token.value == 'var':
          statements.append(self.var_parser())
        elif self.current_token.value == 'print':
          statements.append(self.print_parser())
        elif self.current_token.value == 'while':
          statements.append(self.while_parser())
      elif self.current_token.value == '}':
        self.current_level -= 1
        return statements
      elif self.current_token.category == 'comment':
        continue
      elif self.current_token.category == 'whitespace':
        continue
      elif self.current_token.category == 'error':
        self.syntax_error(self.current_token, 'unexpected token')
      else:
        self.syntax_error(self.current_token, 'unexpected token')
      
      self.current_token = self.tokenizer.tokenize() 

    return statements