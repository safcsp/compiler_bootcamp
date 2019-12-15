from step.parser import *
from step.object import *

class Evaluator:
  def __init__(self):
    pass

  def evaluate(self, syntax_tree):
    pass

  #StepObject
  def evaluate_expr(self, expr):
    if isinstance(expr, LiteralExpression):
      if expr.expression.tid == 'integer_literal':
        return StepObject(int(expr.expression.value), 'integer')
      elif expr.expression.tid == 'boolean_literal':
        if expr.expression.value == 'true':
          return StepObject(True, 'boolean')
        else:
          return StepObject(False, 'boolean')
    elif isinstance(expr, IdentifierExpression):
      return StepObject(1,'integer')
    elif isinstance(expr, BinaryExpression):
      operator = expr.operator.value
      left_operand = self.evaluate_expr(expr.left_exp)
      right_operand = self.evaluate_expr(expr.right_exp)
      if operator == '+':
        if left_operand.vtype == 'integer':
          if right_operand.vtype == 'integer':
            result = left_operand.value + right_operand.value
            return StepObject(result, 'integer')
          elif right_operand.vtype == 'boolean':
            if right_operand.value:
              return StepObject(left_operand.value + 1, 'integer')
            else:
              return StepObject(left_operand.value, 'integer')
        elif left_operand.vtype == 'boolean':
          if right_operand.vtype == 'integer':
            if left_operand.value:
              return StepObject(right_operand.value + 1, 'integer')
            else:
              return StepObject(right_operand.value, 'integer')
          elif right_operand.vtype == 'boolean':
            return StepObject(left_operand.value or right_operand.value, 'boolean')
            # 2 + - 4
    return StepObject(1, 'integer')


