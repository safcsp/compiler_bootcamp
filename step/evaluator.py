from step.parser import *
from step.object import *


class Evaluator:
  def __init__(self):
    pass

  def evaluate(self, syntax_tree, symt):
    for statement in syntax_tree:
      if isinstance(statement, BlockStatement):
        statement.evaluate(self, statement.symt)
      else:
        statement.evaluate(self, symt)

  #StepObject
  def evaluate_expr(self, expr, symt):
    if isinstance(expr, LiteralExpression):
      if expr.expression.tid == 'integer_literal':
        return StepObject(int(expr.expression.value), 'int')
      elif expr.expression.tid == 'boolean_literal':
        if expr.expression.value == 'true':
          return StepObject(True, 'boolean')
        else:
          return StepObject(False, 'boolean')
      elif expr.expression.tid == 'string_literal':
        return StepObject(expr.expression.value, 'string')
    elif isinstance(expr, IdentifierExpression):
      ventry = symt.lookup(expr.expression.value)
      if ventry == None:
        raise Exception('Undefined variable "' + expr.expression.value +'"')
      return ventry.value
    elif isinstance(expr, BinaryExpression):
      operator = expr.operator.value
      left_operand = self.evaluate_expr(expr.left_exp, symt)
      right_operand = self.evaluate_expr(expr.right_exp, symt)
      if operator == '+':
        if left_operand.vtype == 'int':
          if right_operand.vtype == 'int':
            result = left_operand.value + right_operand.value
            return StepObject(result, 'int')
          elif right_operand.vtype == 'boolean':
            if right_operand.value:
              return StepObject(left_operand.value + 1, 'int')
            else:
              return StepObject(left_operand.value, 'int')
          elif right_operand.vtype == 'string':
            return StepObject(str(left_operand.value) + right_operand.value, 'string')
        elif left_operand.vtype == 'boolean':
          if right_operand.vtype == 'int':
            if left_operand.value:
              return StepObject(right_operand.value + 1, 'int')
            else:
              return StepObject(right_operand.value, 'int')
          elif right_operand.vtype == 'boolean':
            return StepObject(left_operand.value or right_operand.value, 'boolean')
          elif right_operand.vtype == 'string':
            raise Exception ('(boolean + string) operation is not allowed')
        elif left_operand.vtype == 'string':
          if right_operand.vtype == 'int':
            result = left_operand.value + str(right_operand.value)
            return StepObject(result, 'string')
          elif right_operand.vtype == 'boolean':
            raise Exception ('(string + boolean) operation is not allowed')
          elif right_operand.vtype == 'string':
            return StepObject(left_operand.value + right_operand.value, 'string')
      elif operator == '<':
        if left_operand.vtype == 'int':
          if right_operand.vtype == 'int':
            result = left_operand.value < right_operand.value
            return StepObject(result, 'boolean')
      elif operator == '>':
        if left_operand.vtype == 'int':
          if right_operand.vtype == 'int':
            result = left_operand.value > right_operand.value
            return StepObject(result, 'boolean')

    return StepObject(1, 'int')


