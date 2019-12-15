
from step.tokenizer import *
from step.parser import *
from step.object import *
from step.evaluator import *

#result = evaluate(expr)

step_keywords = ['var', 'print', 'while', 'true', 'false']
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
parser = Parser(tokenizer)

syntax_tree = parser.parse()
if parser.current_level != 0:
  raise Exception('brackets error')

eva = Evaluator()
result = eva.evaluate_expr(syntax_tree[0].expression)
print(syntax_tree)
