from step.tokenizer import *

class Node:
  pass

class Statement(Node):
  def __init__(self, token=None):
    self.token = token

class Expression(Node):
  def __init__(self, value=None, vtype=None):
    self.value = value
    self.vtype = vtype

class BinaryExpression(Expression):
  def __init__(self, left_exp, operator, right_exp): # 2 + (3 * 5)
    super().__init__()
    self.operator = operator
    self.left_exp = left_exp    
    self.right_exp = right_exp

class UnaryExpression(Expression):
  def __init__(self, operator, exp):
    super().__init__()
    self.operator = operator
    self.expression = exp
  
class LiteralExpression(Expression):
  def __init__(self,exp):
    super().__init__()
    self.expression = exp
  


class IdentifierExpression(Expression):
  def __init__(self,exp):
    super().__init__()
    self.expression = exp
  

class GroupingExpression(Expression):
  def __init__(self,exp):
    super().__init__()
    self.expression = exp
  

class BlockStatement(Statement):
  def __init__(self, token=None, statements=[]):
    super().__init__(token)
    self.statements = statements

class VarStatement(Statement):
  def __init__(self, token, datatype, identifier, expression):
    super().__init__(token)
    self.datatype = datatype
    self.identifer = identifier
    self.expression = expression

#print expression
class PrintStatement(Statement):
  def __init__(self, token, expression):
    super().__init__(token)
    self.expression = expression

class WhileStatement(BlockStatement):
  def __init__(self, token, expression, statements=[]):
    super().__init__(token, statements)
    self.expression = expression

class Parser:
  def __init__(self, tokenizer):
    self.tokenizer = tokenizer
    self.current_token = None
    self.next_token = None
    self.current_level = 0

    self.is_first_token = True
  
  def syntax_error(self, token, message):
    raise Exception('[Step(syntax error)]:' + message + ', ' + token.value + ', line number: ' + str(token.line_number) + ', position: ' + str(token.position))

  def unexpected_token(self):
    self.syntax_error(self.current_token, 'unexpected token')

  def consume(self):

    if self.is_first_token:
      self.current_token = self.tokenizer.tokenize()
      self.is_first_token = False
    else:
      self.current_token = self.next_token
    
    self.next_token = self.tokenizer.tokenize()

  def print_parser(self):
    # print expression
    return PrintStatement(self.current_token, self.expression())

  def match(self, token_value):
    self.consume()
    if self.current_token.value != token_value:
      self.unexpected_token()
    
  def match_category(self, token_category):
    self.consume()
    if self.current_token.category != token_category:
      self.syntax_error(self.current_token, token_category + ' expected')
    
  def while_parser(self):
    # while expression {statements} 
    while_token = self.current_token
    expression = self.expression()
    self.match('{')
    self.current_level += 1
    statements = self.parse()
    #self.match('}')

    return WhileStatement(while_token, expression, statements)
  
  
  def var_parser(self):
    # var datatype id = expression
    var_token = self.current_token
    self.consume()

    if not self.current_token.category == 'keyword' and not self.current_token.value in ['int', 'float', 'string', 'boolean']:
      self.syntax_error(self.current_token, 'datatype expected')

    datatype_token = self.current_token

    self.match_category('identifier')
    identifier_token = self.current_token
    self.match('=')

    return VarStatement(var_token, datatype_token, identifier_token, self.expression() )


  
  def expression(self):  #2 + 5 * 3
    self.consume()
    expr = self.term()
    while self.next_token.value == '+' or self.next_token.value == '-':
      self.consume()
      operator = self.current_token
      self.consume()
      right_expr = self.term()
      expr = BinaryExpression(expr, operator, right_expr)

    return expr
  
  def term(self):
    expr = self.factor()
    while self.next_token.value == '*' or self.next_token.value == '/':
      self.consume()
      operator = self.current_token
      self.consume()
      right_expr = self.factor()
      expr = BinaryExpression(expr, operator, right_expr)
    return expr #(1)
  
  # def unary(self):
  #   if self.current_token.value == '-' or self.current_token.value == '!':
  #     self.consume()
  #     operator = self.current_token
  #     right_expr = self.unary()
  #     expr = UnaryExpression(operator, right_expr)
  #     expr.evaluate(self)
  #     return expr

  #   return self.factor()
    
  def factor(self):
    if self.current_token.category == 'keyword':
      if self.current_token.value in ['true', 'false']:
        token = self.current_token
        token.category = 'literal'
        token.tid = 'boolean_literal'
        return LiteralExpression(token)
    elif self.current_token.category == 'literal':
      if self.current_token.tid == 'integer_literal':
        return LiteralExpression(self.current_token)
    elif self.current_token.category == 'identifier':
      expr = IdentifierExpression(self.current_token)
      return expr
    elif self.current_token.value == '(':
      expr = GroupingExpression(self.expression())
      self.match(')')
      return expr
    
    self.unexpected_token()

  def parse(self):
    statements = []
    self.consume()

    while self.current_token.category != 'EOF':

      if self.current_token.category == 'keyword':
        if self.current_token.value == 'var':
          statements.append(self.var_parser())
        elif self.current_token.value == 'print':
          statements.append(self.print_parser())
        elif self.current_token.value == 'while':
          statements.append(self.while_parser())
        elif self.current_token.value == 'for':
          statements.append(self.for_parser())
      elif self.current_token.value == '}':
        self.current_level -= 1
        return statements
      elif self.current_token.category == 'comment':
        continue
      elif self.current_token.category == 'whitespace':
        continue
      elif self.current_token.category == 'error':
        self.unexpected_token()
      else:
        self.unexpected_token()
      
      self.consume() 

    return statements