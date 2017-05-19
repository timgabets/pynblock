#!/usr/bin/env python

import unittest

from pynblock.tools import raw2str,raw2B, B2raw, xor, key_CV, get_digits_from_string, get_visa_pvv, get_visa_cvv, get_clear_pin, get_pinblock, parityOf, check_key_parity

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

    """
    get_clear_pin()
    """
    def test_get_clear_pin_1234(self):
        self.assertEqual(get_clear_pin(b'0412BCEEDCBA9876', b'881123456789'), b'1234')

    def test_get_clear_pin_non_numeric(self):
        with self.assertRaisesRegex(ValueError, 'PIN contains non-numeric characters'):
            get_clear_pin(b'041267EEDCBA9876', b'881123456789')

    def test_get_clear_pin_pin_length_9(self):
        with self.assertRaisesRegex(ValueError, 'Incorrect PIN length: 9'):
            get_clear_pin(b'091267EEDCBA9876', b'881123456789')

    def test_get_clear_pin_improper_length(self):
        with self.assertRaisesRegex(ValueError, 'Incorrect PIN length: 223'):
            get_clear_pin(b'DF1267EEDCBA9876', b'881123456789')

    """
    get_pinblock()
    """
    def test_get_pinblock_empty_pin(self):
        self.assertEqual(get_pinblock('', '4000001234562000'), None)

    def test_get_pinblock_empty_pan(self):
        self.assertEqual(get_pinblock('1234', ''), None)

    def test_get_pinblock_pin_passed_as_int(self):
        self.assertEqual(get_pinblock(1234, '4000001234562000'), '041234fedcba9dff')

    def test_get_pinblock_cardnumber_passed_as_int(self):
        self.assertEqual(get_pinblock('1234', 4000001234562000), '041234fedcba9dff')    

    def test_get_pinblock_length_4(self):
        self.assertEqual(get_pinblock('1234', '8998811234567890'), '0412bceedcba9876')

    def test_get_pinblock_length_5(self):
        self.assertEqual(get_pinblock('92389', '4000001234562'), '0592789fffedcba9')


    """
    parityOf()
    """
    def test_parityOf_0(self):
        self.assertEqual(parityOf(0), 0)

    def test_parityOf_1(self):
        self.assertEqual(parityOf(2), -1)

    def test_parityOf_xE7(self):
        self.assertEqual(parityOf(int('E7', 16)), 0)

    def test_parityOf_xA3(self):
        self.assertEqual(parityOf(int('A3', 16)), 0)

    def test_parityOf_xB1(self):
        self.assertEqual(parityOf(int('B1', 16)), 0)

    def test_parityOf_xC8(self):
        self.assertEqual(parityOf(int('C8', 16)), -1)    

    """
    check_key_parity()
    """
    def test_check_key_parity_empty_key(self):
        self.assertEqual(check_key_parity(b''), True)

    def test_check_key_parity_xE7(self):
        self.assertEqual(check_key_parity(b'E7'), True)

    def test_check_key_parity_all_bytes_OK(self):
        self.assertEqual(check_key_parity(b'E7A3B1'), True)

    def test_check_key_parity_one_byte_failed_parity_check(self):
        self.assertEqual(check_key_parity(b'E7A3C8B1'), False)

if __name__ == '__main__':
    unittest.main()