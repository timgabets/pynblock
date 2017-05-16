#!/usr/bin/env python

import unittest

from pynblock.tools import raw2str

class TestPynblock(unittest.TestCase):
    def test_raw2str(self):
        self.assertEqual(raw2str(b'\xdf\x12g\xee\xdc\xba\x98v'), 'DF1267EEDCBA9876')


if __name__ == '__main__':
    unittest.main()