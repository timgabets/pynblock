#!/usr/bin/env python

import unittest

from pynblock.tools import raw2str,raw2B, B2raw, xor

class TestPynblock(unittest.TestCase):
    def test_raw2str(self):
        self.assertEqual(raw2str(b'\xdf\x12g\xee\xdc\xba\x98v'), 'DF1267EEDCBA9876')

    def test_raw2B(self):
        self.assertEqual(raw2B(b'\xdf\x12g\xee\xdc\xba\x98v'), b'DF1267EEDCBA9876')

    def test_B2raw(self):
        self.assertEqual(B2raw(b'DF1267EEDCBA9876'), b'\xdf\x12g\xee\xdc\xba\x98v')

    def test_xor(self):
        self.assertEqual(xor(b'0916101000000000', b'C19F07316463054E'), b'C88917216463054E')  

if __name__ == '__main__':
    unittest.main()