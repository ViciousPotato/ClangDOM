import sys

sys.path.append('../')

import unittest
import clangdom

class TestCppParsing(unittest.TestCase):
  def setUp(self):
    self.parser = clangdom.Parser()

  def test_basic_cpp(self):
    unit = self.parser.parse('simple.cpp')
    assert(unit.Functions)

if __name__ == '__main__':
  unittest.main()
