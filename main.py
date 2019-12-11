
from tokenizer import Tokenizer
from parser import Parser

source_code = ''

with open('examples/main.stp') as stp:
  source_code = stp.read(1024)

tokenizer = Tokenizer(source_code, True)
parser = Parser(tokenizer)

syntax_tree = parser.parse()
if parser.current_level != 0:
  raise Exception('brackets error')

print(syntax_tree)