
class Token:
  def __init__(self,tid, value, category, position, line_number):
    self.tid = tid
    self.value = value
    self.category = category
    self.position = position
    self.line_number = line_number

class Tokenizer:
  def __init__(self, source_code):
    self.position = -1
    self.line_number = 1
    self.step_keywords = ['def', 'var', 'int', 'float', 'string', 'boolean', 'if', 'else', 'for', 'while', 'end']
    self.source_code = source_code
    self.length = len(self.source_code)


  def is_eof(self):
    return not self.position < self.length

  def number_tokenizer(self):
    character = self.source_code[self.position]
    token = Token('integer_literal', character, 'literal', self.position, self.line_number)
    self.position += 1
    while not self.is_eof():
      character = self.source_code[self.position]
      if not character.isdigit():
        self.position -= 1
        break
      else: #isdigit
        token.value += character
        self.position += 1

    return token
  
  def identifier_tokenizer(self):
    character = self.source_code[self.position]
    token = Token('id', character, 'identifier', self.position, self.line_number)
    self.position += 1
    while not self.is_eof():
      character = self.source_code[self.position]
      if not (character.isalnum() or character == '_'):
        self.position -= 1
        break
      else:
        token.value += character
        self.position += 1
      
      if token.value in self.step_keywords:
        token.category = 'keyword'
        token.tid = token.value + '_keyword'
        return token

    return token
  
  def comment_tokenizer(self):
    character = self.source_code[self.position]
    token = Token('comment', character, 'comment', self.position, self.line_number)
    self.position += 1
    while not self.is_eof():
      character = self.source_code[self.position]
      if character == '\n':
        self.position -= 1
        break
      else: 
        token.value += character
        self.position += 1

    return token
  
  def whitespace_tokenizer(self):
    character = self.source_code[self.position]
    token = Token('whitespace', character, 'whitespace', self.position, self.line_number)
        
    if character == '\n':
      self.line_number += 1
  
    self.position += 1
    while not self.is_eof():
      character = self.source_code[self.position]
      if not character.isspace():
        self.position -= 1
        break
      else: #isspace
        if character == '\n':
          self.line_number += 1
        token.value += character
        self.position += 1

    return token

  def tokenize(self):
    self.position += 1

    while not self.is_eof():
      character = self.source_code[self.position]
      if character.isdigit(): # tokenize_digit()
        return self.number_tokenizer()
      elif character.isalpha() or character == '_': #Identifier
        return self.identifier_tokenizer()
      elif character.isspace(): #Space
        return self.whitespace_tokenizer()
      elif character == '#': #Comment
        return self.comment_tokenizer()
      else:
        raise Exception('Step Error[' + str(self.line_number) + ', ' + str(self.position) +']: unexpected token "' + character + '"')
        
      self.position += 1
    return Token('EOF','EOF', 'EOF', self.position, self.line_number)

tokenizer = Tokenizer("def var size 10 #This is a comment var x = 2")
token = tokenizer.tokenize()
while token.category != 'EOF':
  print('category ->', token.category, 'value ->', token.value, 'position ->', token.position, 'line number ->', token.line_number)
  token = tokenizer.tokenize()
  