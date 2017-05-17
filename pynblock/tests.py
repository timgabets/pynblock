#!/usr/bin/env python

import unittest

from pynblock.tools import raw2str,raw2B, B2raw, xor, key_CV

class TestPynblock(unittest.TestCase):
    def test_raw2str(self):
        self.assertEqual(raw2str(b'\xdf\x12g\xee\xdc\xba\x98v'), 'DF1267EEDCBA9876')

    def test_raw2B(self):
        self.assertEqual(raw2B(b'\xdf\x12g\xee\xdc\xba\x98v'), b'DF1267EEDCBA9876')

    def test_B2raw(self):
        self.assertEqual(B2raw(b'DF1267EEDCBA9876'), b'\xdf\x12g\xee\xdc\xba\x98v')

    def test_xor(self):
        self.assertEqual(xor(b'0916101000000000', b'C19F07316463054E'), b'C88917216463054E')

    def test_key_CV_default_kcv_length(self):
        self.assertEqual(key_CV(b'E6F1081FEA4C402CC192B65DE367EC3E'), b'212CF9')

    def test_key_CV_4(self):
        self.assertEqual(key_CV(b'E6F1081FEA4C402CC192B65DE367EC3E', 4), b'212C')

    def test_key_CV_6(self):
        self.assertEqual(key_CV(b'E6F1081FEA4C402CC192B65DE367EC3E', 6), b'212CF9')

    def test_key_CV_16(self):
        self.assertEqual(key_CV(b'E6F1081FEA4C402CC192B65DE367EC3E', 16), b'212CF9158251CDD3')

if __name__ == '__main__':
    unittest.main()