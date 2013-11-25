import sys

sys.path.append('../')

import unittest
import clangdom

class TestCppParsing(unittest.TestCase):
  def setUp(self):
    self.parser = clangdom.Parser()

  def test_basic_cpp(self):
    unit = self.parser.parse('simple.cpp')
    self.assertEquals(len(unit.functions), 1)
    f = unit.functions[0]
    self.assertEquals(f.name, "main")
    self.assertEquals(len(f.args), 0)


  def test_include_files(self):
    unit = self.parser.parse('include.cpp')
    self.assertEquals(len(unit.includes), 1)
    f = unit.includes[0].include.name
    self.assertTrue(f.endswith('vector'))
    
if __name__ == '__main__':
  unittest.main()
