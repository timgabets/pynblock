#!/usr/bin/env python

import unittest

from pynblock.tools import raw2str,raw2B, B2raw, xor, key_CV, get_digits_from_string, get_visa_pvv, get_visa_cvv

class TestPynblock(unittest.TestCase):
    def test_raw2str(self):
        self.assertEqual(raw2str(b'\xdf\x12g\xee\xdc\xba\x98v'), 'DF1267EEDCBA9876')

    def test_raw2B(self):
        self.assertEqual(raw2B(b'\xdf\x12g\xee\xdc\xba\x98v'), b'DF1267EEDCBA9876')

    def test_B2raw(self):
        self.assertEqual(B2raw(b'DF1267EEDCBA9876'), b'\xdf\x12g\xee\xdc\xba\x98v')

    def test_xor(self):
        self.assertEqual(xor(b'0916101000000000', b'C19F07316463054E'), b'C88917216463054E')

    """
    key_CV()
    """
    def test_key_CV_default_kcv_length(self):
        self.assertEqual(key_CV(b'E6F1081FEA4C402CC192B65DE367EC3E'), b'212CF9')

    def test_key_CV_4(self):
        self.assertEqual(key_CV(b'E6F1081FEA4C402CC192B65DE367EC3E', 4), b'212C')

    def test_key_CV_6(self):
        self.assertEqual(key_CV(b'E6F1081FEA4C402CC192B65DE367EC3E', 6), b'212CF9')

    def test_key_CV_16(self):
        self.assertEqual(key_CV(b'E6F1081FEA4C402CC192B65DE367EC3E', 16), b'212CF9158251CDD3')

    """
    get_digits_from_string()
    """
    def test_get_digits_from_string(self):
        self.assertEqual(get_digits_from_string('59EF34AD722C0556F7F6FBD4A76D38E6', 4), '5934')

    def test_get_pvv_digits_from_mixed_string(self):
        self.assertEqual(get_digits_from_string('EEFADCFFFBD7ADECAB9FBB', 4), '7944')

    def test_get_digits_from_string_letters_only(self):
        self.assertEqual(get_digits_from_string('EFADCFFFBDADECABFBB', 4), '4503')

    def test_get_digits_from_string_letters_only_3(self):
        self.assertEqual(get_digits_from_string('EFADCFFFBDADECABFBB', 3), '450')

    """
    get_visa_pvv()
    """
    def test_get_visa_pvv(self):
        self.assertEqual(get_visa_pvv(b'4761260000000134', b'1', b'1234', b'DEADDEADDEADDEADBEAFBEAFBEAFBEAF'), b'8289')

    def test_get_visa_pvv_incorrect_key(self):
        with self.assertRaisesRegex(ValueError, 'Incorrect key length'):
            get_visa_pvv(b'4761260000000134', b'1', b'1234', b'DEADDEADDEADDEADBEAFBEAFBEAF')

    """
    get_visa_cvv()
    """
    def test_get_visa_cvv(self):
        self.assertEqual(get_visa_cvv(b'4433678298261175', b'0916', b'101', b'4C37C8319D76ADAB58D9431543C2165B'), '478')

if __name__ == '__main__':
    unittest.main()