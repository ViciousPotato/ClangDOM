import os
import sys

def parent_dir():
  return os.path.abspath(
    os.path.join(
      os.path.dirname(os.path.abspath(__file__)),
      '../'
    )
  )

sys.path.append(parent_dir())

import unittest
import clangdom

def test_file(f):
  return os.path.join(
    os.path.dirname(os.path.abspath(__file__)), f)

class TestCppParsing(unittest.TestCase):
  def setUp(self):
    self.parser = clangdom.Parser()

  def test_basic_cpp(self):
    unit = self.parser.parse(test_file('simple.cpp'))
    self.assertEquals(len(unit.functions), 2)
    f = unit.functions[0]
    self.assertEquals(f.name, "f")
    self.assertEquals(len(f.params), 1)
    self.assertEquals(f.params[0].name, 'a')
    self.assertEquals(f.params[0].type, 'int')

    f = unit.functions[1]
    self.assertEquals(f.name, "main")
    self.assertEquals(len(f.params), 0)

  def test_include_files(self):
    unit = self.parser.parse(test_file('include.cpp'))
    self.assertEquals(len(unit.includes), 4)
    self.assertTrue(unit.includes[0].name.endswith('vector'))
    self.assertTrue(unit.includes[1].name.endswith('undefined'))
    self.assertTrue(unit.includes[2].name.endswith('some/fairy/land'))
    self.assertTrue(unit.includes[3].name.endswith('../and/its/parent'))

if __name__ == '__main__':
  unittest.main()
