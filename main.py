
from tokenizer import Tokenizer

source_code = ''

with open('examples/main.stp') as stp:
  source_code = stp.read(1024)

tokenizer = Tokenizer(source_code)
token = tokenizer.tokenize()

style = {
  'keyword': 'color:blue',
  'punctuation': 'color:red',
  'operator': 'color:red',
  'comment' : 'color:gray',
  'identifier': 'color: #F94',
  'literal': 'color:black; font-weight:bold',
  'error' : 'color: white; background-color:red; padding: 8px;',
  'whitespace': '',
  'EOF': ''
}

with open('examples/main.html', 'w') as hstp:
  hstp.write("<html><body><code><pre>")

  while token.category != 'EOF':
    hstp.write('<span style="'+style[token.category]+'">'+token.value+'</span>')
    token = tokenizer.tokenize()

  hstp.write("</pre></code></body></html>")
  

  