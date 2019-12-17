from step.tokenizer import *
from step.parser import *
from step.evaluator import *
from step.symboltable import *

class StepCompiler:
  def __init__(self):
    self.step_keywords = ['var', 'let', 'print', 'while', 'true', 'false','null','int', 'float', 'string', 'boolean', 'fun']
    self.step_punctuations = {
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
  
  def compile(self):
    pass
  
  def run(self, source_path):

    source_code = ''
    with open(source_path) as stp:
      source_code = stp.read(1024)

    tokenizer = Tokenizer(source_code,self.step_keywords,self.step_punctuations, True)
    symt = SymbolTable('global', 'module')
    parser = Parser(tokenizer, symt)
    syntax_tree = parser.statements()
    self.analyze_convension(symt)
    eva = Evaluator()
    eva.evaluate(syntax_tree, symt)
  
  def analyze_convension(self, symt):
    for identifier, entry in symt.entriers.items():
      if len(identifier) < 3:
        raise Exception("analyzer: identifier name must be 3 or more characters")

