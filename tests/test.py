import unittest
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import simpleflags

class Test(unittest.TestCase):
    def setUp(self):
        self.Flags = simpleflags.Flags()
        self.argv = sys.argv[:]

    def tearDown(self):
        sys.argv = self.argv

    def testDefineBoolean(self):
        self.Flags.define_bool('test_true', True, 'Test define bool True')
        self.Flags.define_bool('test_false', False, 'Test define bool False')
        self.assertTrue(self.Flags.test_true)
        self.assertFalse(self.Flags.test_false)

    def testDefineInt(self):
        self.Flags.define_int('test_zero', 0, 'Test define int 0')
        self.Flags.define_int('test_pos', 999999, 'Test define int 999999')
        self.Flags.define_int('test_neg', -892389, 'Test define int -892389')
        self.assertTrue(self.Flags.test_zero == 0)
        self.assertTrue(self.Flags.test_pos == 999999)
        self.assertTrue(self.Flags.test_neg == -892389)

    def testDefineString(self):
        self.Flags.define_string('test_string_empty', '', 'Test define string empty')
        self.Flags.define_string('test_string_nonempty', 'hello world!', 'Test define string nonempty')
        self.assertTrue(self.Flags.test_string_empty == '')
        self.assertTrue(self.Flags.test_string_nonempty == 'hello world!')

    def testDefineFloat(self):
        self.Flags.define_float('test_float', 3.14, 'Test define float 3.14')
        self.assertTrue(self.Flags.test_float == 3.14)

if __name__ == "__main__":
    unittest.main()
