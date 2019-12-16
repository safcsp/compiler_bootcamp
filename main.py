
from step.tokenizer import *
from step.parser import *
from step.object import *
from step.evaluator import *

step_keywords = ['var', 'let', 'print', 'while', 'true', 'false','null','int', 'float', 'string', 'boolean']
step_punctuations = {
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
source_code = ''

with open('examples/main.stp') as stp:
  source_code = stp.read(1024)

tokenizer = Tokenizer(source_code,step_keywords,step_punctuations, True)
symt = SymbolTable('global')
parser = Parser(tokenizer, symt)

syntax_tree = parser.parse()
if parser.current_level != 0:
  raise Exception('brackets error')

eva = Evaluator()
eva.evaluate(syntax_tree, symt)
print('...')