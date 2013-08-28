import sys
# See http://clang.llvm.org/docs/IntroductionToTheClangAST.html
from clang.cindex import Index, CursorKind

class Object(object):
  def __setattr__(self, name, value):
    self.__dict__[name] = value

  def __getattr__(self, name):
    self.__dict__.get(name, None)

class Decl(object):
  """docstring for Decl"""
  def __init__(self, arg):
    super(Decl, self).__init__()
    self.arg = arg
    
class Type(object):
  """docstring for Type"""
  def __init__(self, arg):
    super(Type, self).__init__()
    self.arg = arg

class DeclContext(object):
  """docstring for DeclContext"""
  def __init__(self, arg):
    super(DeclContext, self).__init__()
    self.arg = arg
    
class Stmt(object):
  """docstring for Stmt"""
  def __init__(self, arg):
    super(Stmt, self).__init__()
    self.arg = arg

class Function(object):
  def __init__(self, name, args=[], returnType=""):
    self.name = name
    self.args = args
    self.returnType = returnType
    super(Function, self).__init__()

  def __str__(self):
    return "%s %s(%s)" % (returnType, name, ",".join(args))

class Parser(object):
  def __init__(self):
    self.index = Index.create()
    self.ast   = Object()
    self.mapping = {

    }
    super(Parser, self).__init__()

  def parse(self, src):
    unit = self.index.parse(src)
    self.visit(unit.cursor)
    return self.ast

  def visit(self, node):
    for child in node.get_children():
      if child.kind == CursorKind.FUNCTION_DECL:
        self.ast.functions = self.ast.functions or []
        self.ast.functions.append(Function(child.spelling))

      self.visit(child)


def visit(node, depth=1):
  print '    ' * depth, node.kind, node.xdata, node.spelling
  for c in node.get_children():
    visit(c, depth+1)

if __name__ == '__main__':
  index = Index.create()
  u = index.parse(sys.argv[1])
  visit(u.cursor)

  parser = Parser()
  u = parser.parse(sys.argv[1])
  print u.functions


    