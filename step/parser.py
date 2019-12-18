from step.tokenizer import *
from step.symboltable import *

class Node:
  pass

class Statement(Node):
  def __init__(self, token=None):
    self.token = token
  def evaluate(self, evaluator, symt):
    pass

class ExpressionStatement(Statement):
  def __init__(self, expression):
    self.expression = expression

class Expression(Node):
  def __init__(self, value=None, vtype=None):
    self.value = value
    self.vtype = vtype

class CallExpression(Expression):
  def __init__(self, identifier, arguments=[]):
    self.identifier = identifier
    self.arguments = arguments

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
  def __init__(self, token=None, statements=[], symt_name= None,symt_type=None, parent_symt=None):
    super().__init__(token)
    self.statements = statements
    self.symt = SymbolTable(symt_name,symt_type, parent_symt)

class VarStatement(Statement):
  def __init__(self, token, datatype, identifier, expression):
    super().__init__(token)
    self.datatype = datatype
    self.identifer = identifier
    self.expression = expression
  
  def evaluate(self, evaluator, symt):
    result = evaluator.evaluate_expr(self.expression, symt)
    entry = symt.lookup(self.identifer.value)
    if entry.datatype != result.vtype:
      raise Exception("Invalid var expression")
    entry.value = result

class LetStatement(Statement):
  def __init__(self, token, identifier, expression):
    super().__init__(token)
    self.identifer = identifier
    self.expression = expression
  
  def evaluate(self, evaluator, symt):
    result = evaluator.evaluate_expr(self.expression, symt)
    entry = symt.lookup(self.identifer.value)
    if entry.datatype != result.vtype:
      raise Exception("Invalid let expression")

    entry.value = result
    

class PrintStatement(Statement):
  def __init__(self, token, expression):
    super().__init__(token)
    self.expression = expression
  
  def evaluate(self, evaluator, symt):
    result = evaluator.evaluate_expr(self.expression, symt)
    print(result.value)
  
class ReturnStatement(Statement):
  def __init__(self, token, expression):
    super().__init__(token)
    self.expression = expression
  
  def evaluate(self, evaluator, symt):
    pass


class WhileStatement(BlockStatement):
  def __init__(self, token, expression, statements=[], parent_symt=None):
    super().__init__(token,statements, 'while','loop',  parent_symt)
    self.expression = expression

  def evaluate(self, evaluator, symt):
    result = evaluator.evaluate_expr(self.expression, symt)
    if result.vtype != 'boolean':
      raise Exception('Invalid while expression')

    while result.value:
      evaluator.evaluate(self.statements, symt)
      result = evaluator.evaluate_expr(self.expression, symt)
      if result.vtype != 'boolean':
        raise Exception('Invalid while expression')


class FunStatement(BlockStatement):
  def __init__(self, token, datatype, identifier, parameters=[], statements=[], parent_symt=None):
    super().__init__(token,statements, identifier.value, 'fun', parent_symt)
    self.datatype = datatype
    self.identifier = identifier
    self.parameters = parameters

class Parser:
  def __init__(self, tokenizer, symt):
    self.tokenizer = tokenizer
    self.current_token = None
    self.next_token = None
    self.current_level = 0

    self.is_first_token = True
    self.symt = symt
    self.active_symt = symt
  
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
  
  def return_parser(self):
    if self.active_symt.type_lookup('fun') == None:
      raise Exception("'return' statement must be used inside a function.")
    return ReturnStatement(self.current_token, self.expression())


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
    #self.match('}')

    while_statement = WhileStatement(while_token, expression, None, self.active_symt)
    self.active_symt = while_statement.symt
    while_statement.statements = self.parse()
    return while_statement
  
  # <fun-statement> ::= FUN <datatype> ID ([<parameters>]){<statements>}
  # <parameters> ::= <parameter> | <parameter>, <parameters>
  # <parameter> ::= <datatype> ID

  def fun_parser(self):
    if self.current_level != 0:
      raise Exception('Invalid function definition. Function must be inside global scope.')
    
    fun_token = self.current_token

    self.consume()
    if not self.current_token.category == 'keyword' and not self.current_token.value in ['int', 'float', 'string', 'boolean']:
      self.syntax_error(self.current_token, 'datatype expected')

    datatype_token = self.current_token
    self.match_category('identifier')
    identifier_token = self.current_token

    fun_statement = FunStatement(fun_token, datatype_token, identifier_token, [], None, self.active_symt)
    self.active_symt = fun_statement.symt

    self.match('(')
    parameters = []
    if self.next_token.value == ')':
      self.match(')')
    else:
      parameters = self.parameters_parser()
      self.match(')')
    
    self.match('{')

    self.current_level += 1

    entry = FunctionEntry(datatype_token.value, parameters, fun_statement.symt)
    self.symt.insert(identifier_token.value, entry)
    fun_statement.parameters = parameters
    fun_statement.statements = self.parse()
    return fun_statement

  # <parameters> ::= <parameter> | <parameter>, <parameters>

  def parameters_parser(self):
    parameters = []
    parameters.append(self.parameter_parser())
    while self.next_token.value == ',':
      self.consume()
      parameters.append(self.parameter_parser())
    
    return parameters
  
  # <parameter> ::= <datatype> ID

  def parameter_parser(self):
    self.consume()
    if not self.current_token.category == 'keyword' and not self.current_token.value in ['int', 'float', 'string', 'boolean']:
      self.syntax_error(self.current_token, 'datatype expected')
    
    datatype = self.current_token
    self.match_category('identifier')

    parameter = {
      'datatype': datatype,
      'name' : self.current_token
    }

    entry = ParameterEntry(datatype, 0)
    self.active_symt.insert(self.current_token.value, entry)
    
    return parameter
  
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

    ventry = VariableEntry(datatype_token.value, 0, 0)
    self.active_symt.insert(identifier_token.value, ventry)

    return VarStatement(var_token, datatype_token, identifier_token, self.expression() )


  def let_parser(self):
    # let id = expression
    let_token = self.current_token

    self.match_category('identifier')
    identifier_token = self.current_token

    ventry = self.active_symt.lookup(identifier_token.value)
    if ventry == None:
      self.syntax_error(identifier_token, "undefined variable")
    
    self.match('=')
    
    return LetStatement(let_token, identifier_token, self.expression() )
  

  def expression(self):  #2 + 5 * 3
    self.consume()
    expr = self.relational()
    while self.next_token.value == '+' or self.next_token.value == '-':
      self.consume()
      operator = self.current_token
      self.consume()
      right_expr = self.relational()
      expr = BinaryExpression(expr, operator, right_expr)

    return expr

  def relational(self):  #2 + 5 * 3
    expr = self.term()
    while self.next_token.value == '>' or self.next_token.value == '<':
      self.consume()
      operator = self.current_token
      self.consume()
      right_expr = self.term()
      expr = BinaryExpression(expr, operator, right_expr)

    return expr
  
  def term(self):
    expr = self.postfix()
    while self.next_token.value == '*' or self.next_token.value == '/':
      self.consume()
      operator = self.current_token
      self.consume()
      right_expr = self.postfix()
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
  
  def postfix(self):
    expr = self.factor()
    if isinstance(expr, IdentifierExpression) and self.next_token.value == '(':    
      self.match('(')
      if self.next_token.value == ')':
        arguments = []
      else:
        arguments = self.arguments_parser()
      
      self.match(')')
      return CallExpression(expr, arguments)

    return expr

  def arguments_parser(self):
    arguments = [self.expression()]
    while self.next_token.value == ',':
      self.match(',')
      arguments.append(self.expression())
    
    return arguments

  def factor(self):
    if self.current_token.category == 'literal':
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
        elif self.current_token.value == 'let':
          statements.append(self.let_parser())
        elif self.current_token.value == 'print':
          statements.append(self.print_parser())
        elif self.current_token.value == 'while':
          statements.append(self.while_parser())
        elif self.current_token.value == 'for':
          statements.append(self.for_parser())
        elif self.current_token.value == 'fun':
          statements.append(self.fun_parser())
        elif self.current_token.value == 'return':
          statements.append(self.return_parser())
      elif self.current_token.value == '}':
        self.current_level -= 1
        self.active_symt = self.active_symt.parent
        return statements
      elif self.current_token.category == 'error':
        self.unexpected_token()
      elif self.current_token.category == 'identifier':
        expr = self.postfix()
        statements.append(ExpressionStatement(expr))
      
      self.consume() 

    return statements
  
  def statements(self):
    syntax_tree = self.parse()
    if self.current_level != 0:
      raise Exception('brackets error')
    return syntax_tree