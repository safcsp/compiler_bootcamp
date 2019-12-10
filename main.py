
from tokenizer import Tokenizer
from parser import Parser

source_code = ''

with open('examples/main.stp') as stp:
  source_code = stp.read(1024)

tokenizer = Tokenizer(source_code, True)
parser = Parser(tokenizer)

syntax_tree = parser.parse()
print(syntax_tree)

# token = tokenizer.tokenize()

# style = {
#   'keyword': 'color:blue',
#   'punctuation': 'color:red',
#   'operator': 'color:red',
#   'comment' : 'color:gray',
#   'identifier': 'color: #F94',
#   'literal': 'color:black; font-weight:bold',
#   'error' : 'color: black; border-bottom: 1px dashed red; padding-bottom: -2px;',
#   'whitespace': '',
#   'EOF': ''
# }

# with open('examples/main.html', 'w') as hstp:
#   hstp.write("<html><body><code><pre>")

#   while token.category != 'EOF':
#     hstp.write('<span style="'+style[token.category]+'">'+token.value+'</span>')
#     token = tokenizer.tokenize()

#   hstp.write("</pre></code></body></html>")
  

  