
class Token:
  def __init__(self, value, category, position, line_number):
    self.value = value
    self.category = category
    self.position = position
    self.line_number = line_number

#digit -> [0-9]+
position = -1
line_number = 1
step_keywords = ['def', 'var', 'int', 'float', 'string', 'boolean', 'if', 'else', 'for', 'while', 'end']
def tokenize(source_code):
  global position
  global line_number
  global step_keywords

  position += 1

  length = len(source_code)
  while position < length:
    character = source_code[position]
    if character.isdigit(): # tokenize_digit()
      number_token = Token(character, 'literal', position, line_number)
      position += 1
      while(position < length):
        character = source_code[position]
        if not character.isdigit():
          position -= 1
          break
        else: #isdigit
          number_token.value += character
          position += 1

      return number_token
    elif character.isalpha() or character == '_': #Identifier
      id_token = Token(character, 'identifier', position, line_number)
      position += 1
      while(position < length):
        character = source_code[position]
        if not (character.isalnum() or character == '_'):
          position -= 1
          break
        else: #isid
          id_token.value += character
          position += 1

      if id_token.value in step_keywords:
        id_token.category = 'keyword'
      return id_token
    elif character.isspace(): #Space
      space_token = Token(character, 'space', position, line_number)
      
      if character == '\n':
        line_number += 1
     
      position += 1
      while(position < length):
        character = source_code[position]
        if not (character.isspace()):
          position -= 1
          break
        else: #isspace
          if character == '\n':
            line_number += 1
          space_token.value += character
          position += 1

      return space_token
    elif character == '#': #Comment
      comment_token = Token('', 'comment', position, line_number)
      position += 1
      while(position < length):
        character = source_code[position]
        if character == '\n':
          position -= 1
          break
        else: #iscomment
          comment_token.value += character
          position += 1

      return comment_token
    else:
      raise Exception('Step Error[' + str(line_number) + ', ' + str(position) +']: unexpected token "' + character + '"')
      
    position += 1
  return Token('EOF', 'EOF', position, line_number)

#.............\n
source_code = "def var size 10 #This is a comment var x = 2"
token = tokenize(source_code)
while token.category != 'EOF':
  print('category ->', token.category, 'value ->', token.value, 'position ->', token.position, 'line number ->', token.line_number)
  token = tokenize(source_code)
  
print(token.value)