
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
v = VarStatement(Token('var_keyword', 'var', 'keyword', 0, 1), Token('int_keyword', 'int', 'keyword', 0, 1),Token('id', 'fooBar', 'identifier', 0, 1), LiteralExpression(Token('integer_literal', '75', 'literal', 0, 1)))
ventry = VariableEntry('int', 0, 0)
symt.insert('fooBar', ventry)

syntax_tree = [v, syntax_tree[0]]

# var int fooBar = 75
if parser.current_level != 0:
  raise Exception('brackets error')
eva = Evaluator()
eva.evaluate(syntax_tree, symt)
print('...')

# 2 + 3

# expr = BinaryExpression(LiteralExpression(Token('integer_literal', '2', 'literal', 0, 1)),Token('plus', '+', 'operator', 0, 1),LiteralExpression(Token('integer_literal', '3', 'literal', 0, 1)))
# print(eva.evaluate_expr(expr, symt).value)