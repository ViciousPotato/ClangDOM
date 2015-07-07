import re
import sys
import copy
# See http://clang.llvm.org/docs/IntroductionToTheClangAST.html
from clang.cindex import Index, CursorKind, TranslationUnit

def auto_load():
  """ Find libclang and load it """
  if sys.startswith('linux'):
    pass

class Object(object):
  def __setattr__(self, name, value):
    self.__dict__[name] = value

  def __getattr__(self, name):
    self.__dict__.get(name, None)

class Unit(Object):
  pass

class Decl(object):
  def __init__(self, arg):
    super(Decl, self).__init__()
    self.arg = arg
    
class Type(object):
  def __init__(self, arg):
    super(Type, self).__init__()
    self.arg = arg

class DeclContext(object):
  def __init__(self, arg):
    super(DeclContext, self).__init__()
    self.arg = arg
    
class Stmt(object):
  def __init__(self, arg):
    super(Stmt, self).__init__()
    self.arg = arg

class FunctionParam(object):
  def __init__(self, name, type):
    self.name = name
    self.type = type
    super(Function, self).__init__()

  def __str__(self):
    return "%s %s" % (self.type, self.name)

class Function(object):
  """ http://clang.llvm.org/doxygen/classclang_1_1FunctionDecl.html """
  def __init__(self, name, params=[], returnType=""):
    self.name = name
    self.params = params
    self.returnType = returnType
    super(Function, self).__init__()

  def __str__(self):
    return "%s %s(%s)" % (returnType, name, ",".join(params))

  @classmethod
  def parse(cursor):
    func_name = cursor.spelling
    result_type = cursor.result_type.spelling
    args = [] 
    for arg in cursor.get_arguments():
      name = arg.spelling
      type = arg.type.spelling
      args.append(FunctionParam(name, type))
    return Function(func_name, args, result_type)

class IncludeFile(object):
  def __init__(self, name, type="absolute"):
    self.name = name
    self.type = type
    super(IncludeFile, self).__init__()

class Parser(object):
  def __init__(self):
    self.index = Index.create()
    self.ast = Object()
    self.mapping = {

    }
    super(Parser, self).__init__()

  def parse_includes(self, src, unit):
    # Parse includes
    # The problem with below commented approach is that diagnostics don't contain all include files.
    """
    for diag in unit.diagnostics:
      m = re.match(r'\'(.+?)\' file not found', diag.spelling)
      if m:
        self.ast.includes.append(m.groups()[0])
    """
    self.ast.includes = [IncludeFile(i.include.name) for i in unit.get_includes() if i.depth == 1]
    content = file(src).read()
    content = re.sub(r'/\*.+?\*/', '', content, flags=re.S) # Remove /* comments
    includes = []
    included = {}
    for line in content.splitlines():
      m = re.match(r'^\s*#include\s*(<|")(.+?)(>|")\s*', line)
      if m:
        l, f, r = m.groups()
        fullname = l + f + r
        if included.has_key(fullname):
          continue
        if l == "<":
          includes.append(IncludeFile(f))
        else:
          includes.append(IncludeFile(f, "relative"))
        included[fullname] = 1
    self.ast.includes = includes

    # include statement is not in comments or literal string

  def parse_function(self, cursor):
    for arg in cursor.get_arguments():
      pass

  def parse(self, src):
    unit = self.index.parse(src,
      args = ['-Xclang', '-ast-dump', '-fsyntax-only'],
      options = TranslationUnit.PARSE_INCOMPLETE)

    self.parse_includes(src, unit)

    self.visit(unit.cursor)
    return self.ast

  def visit(self, node):
    for child in node.get_children():
      if child.kind == CursorKind.FUNCTION_DECL:
        self.parse_function(child)
        self.ast.functions = self.ast.functions or []
        self.ast.functions.append(Function.parse(child))

      self.visit(child)

def visit(node, depth=1):
  print '    ' * depth, node.kind, node.xdata, node.spelling
  for c in node.get_children():
    visit(c, depth+1)

if __name__ == '__main__':
  index = Index.create()
  u = index.parse(sys.argv[1])
  #visit(u.cursor)

  parser = Parser()
  u = parser.parse(sys.argv[1])
  print u.functions