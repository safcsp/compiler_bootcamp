
class Token:
  def __init__(self,tid, value, category, position, line_number):
    self.tid = tid
    self.value = value
    self.category = category
    self.position = position
    self.line_number = line_number

class Tokenizer:
  def __init__(self, source_code, keywords =[], punctuations ={}, ignore_whitespace=False):
    self.position = -1
    self.line_number = 1
    self.ignore_whitespace = ignore_whitespace

    self.step_keywords = keywords
    self.punctuations = punctuations
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

  def gt_tokenizer(self):
    return self.one_or_two_tokenizer('gt', '=', 'gte')
  
  def lt_tokenizer(self):
    return self.one_or_two_tokenizer('lt', '=', 'lte')


  def one_or_two_tokenizer(self, first_tid, peek_character, second_tid):
    character = self.source_code[self.position]
    token = Token(first_tid, character, 'operator', self.position, self.line_number)
    peek_value = self.peek()
    if peek_value == peek_character:
      self.position += 1
      token.value += self.source_code[self.position]
      token.tid = second_tid

    return token

  def plus_tokenizer(self):
    return self.one_or_two_tokenizer('plus', '+', 'plusplus')
  
  def minus_tokenizer(self):
    return self.one_or_two_tokenizer('minus', '-', 'minusminus')
  
  def multiplication_tokenizer(self):
    character = self.source_code[self.position]
    token = Token('multiplication', character, 'operator', self.position, self.line_number)
    return token
  
  def division_tokenizer(self):
    character = self.source_code[self.position]
    token = Token('division', character, 'operator', self.position, self.line_number)
    return token
  
  def equal_tokenizer(self): 
    return self.one_or_two_tokenizer('assignment', '=', 'equalequal')
  
  def not_tokenizer(self): 
    return self.one_or_two_tokenizer('not', '=', 'notequal')

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
        if not self.ignore_whitespace:
          return token
      elif character == '#': #Comment
        return self.comment_tokenizer()
      elif character == '+':
        return self.plus_tokenizer()
      elif character == '-':
        return self.minus_tokenizer()
      elif character == '*':
        return self.multiplication_tokenizer()
      elif character == '/':
        return self.division_tokenizer()
      elif character in self.punctuations.keys():
        return self.punctuation_tokenizer()
      elif character == '=':
        return self.equal_tokenizer()
      elif character == '>':
        return self.gt_tokenizer()
      elif character == '<':
        return self.lt_tokenizer()
      elif character == '!':
        return self.not_tokenizer()
      else:
        return Token('error', character, 'error', self.position, self.line_number)
        
      self.position += 1
    return Token('EOF','EOF', 'EOF', self.position, self.line_number)