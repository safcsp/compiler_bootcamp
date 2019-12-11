
class Token:
  def __init__(self,tid, value, category, position, line_number):
    self.tid = tid
    self.value = value
    self.category = category
    self.position = position
    self.line_number = line_number

class Tokenizer:
  def __init__(self, source_code, ignore_whitespace=False):
    self.position = -1
    self.line_number = 1
    self.ignore_whitespace = ignore_whitespace

    self.step_keywords = ['let', 'var', 'int', 'float', 'string', 'boolean', 'if', 'else', 'for', 'while', 'end', 'print', 'def', 'return']
    self.punctuations = {
      '(' : 'left_paren',
      ')' : 'right_paren',
      '[' : 'left_square',
      ']' : 'right_square',
      ';' : 'semicolon',
      ',' : 'comma',
      '{' : 'left_curly',
      '}' : 'right_curly',
      ':' : 'colon'
    }
    self.source_code = source_code
    self.length = len(self.source_code)


  def is_eof(self):
    return not self.position < self.length
  
  def is_peekable(self):
    return (self.position + 1) < self.length
  
  def peek(self):
    if self.is_peekable():
      return self.source_code[self.position + 1]
    return '\0'


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

  def plus_tokenizer(self):
    character = self.source_code[self.position]
    token = Token('plus', character, 'operator', self.position, self.line_number)
    peek_value = self.peek()
    if peek_value == '+':
      self.position += 1
      token.value += self.source_code[self.position]
      token.tid = 'plusplus'

    return token
  
  def equal_tokenizer(self): 
    character = self.source_code[self.position]
    token = Token('assignment', character, 'operator', self.position, self.line_number)
    if self.peek() == '=':
      self.position += 1
      token.value += self.source_code[self.position]
      token.tid = 'equalequal'
    return token

  def punctuation_tokenizer(self): 
    character = self.source_code[self.position]
    tid = self.punctuations[character]
    return Token(tid, character, 'punctuation', self.position, self.line_number)
  
      
  def tokenize(self):
    self.position += 1

    while not self.is_eof():
      character = self.source_code[self.position]
      if character.isdigit(): # tokenize_digit()
        return self.number_tokenizer()
      elif character.isalpha() or character == '_': #Identifier
        return self.identifier_tokenizer()
      elif character.isspace(): #Space
        token = self.whitespace_tokenizer()
        if not self.ignore_whitepsace:
          return token
      elif character == '#': #Comment
        return self.comment_tokenizer()
      elif character == '+':
        return self.plus_tokenizer()
      elif character in self.punctuations.keys():
        return self.punctuation_tokenizer()
      elif character == '=':
        return self.equal_tokenizer()
      else:
        return Token('error', character, 'error', self.position, self.line_number)
        
      self.position += 1
    return Token('EOF','EOF', 'EOF', self.position, self.line_number)