import os
import sys

sys.path.append('../')

import unittest
import clangdom

def test_file(f):
  return os.path.join(
    os.path.dirname(os.path.abspath(__file__)), f)

class TestCppParsing(unittest.TestCase):
  def setUp(self):
    self.parser = clangdom.Parser()

  def test_basic_cpp(self):
    print test_file('simple.cpp')
    unit = self.parser.parse(test_file('simple.cpp'))
    self.assertEquals(len(unit.functions), 1)
    f = unit.functions[0]
    self.assertEquals(f.name, "main")
    self.assertEquals(len(f.args), 0)

  def test_include_files(self):
    unit = self.parser.parse(test_file('include.cpp'))
    self.assertEquals(len(unit.includes), 4)
    self.assertTrue(unit.includes[0].name.endswith('vector'))
    self.assertTrue(unit.includes[1].name.endswith('undefined'))
    self.assertTrue(unit.includes[2].name.endswith('some/fairy/land'))
    self.assertTrue(unit.includes[3].name.endswith('../and/its/parent'))

if __name__ == '__main__':
  unittest.main()
