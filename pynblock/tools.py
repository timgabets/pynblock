#!/usr/bin/env python

from binascii import hexlify, unhexlify
from Crypto.Cipher import DES, DES3


def raw2str(raw_data):
    """
    Convert raw binary data to string representation, e.g. b'\xdf\x12g\xee\xdc\xba\x98v'-> 'DF1267EEDCBA9876'
    """
    return hexlify(raw_data).decode('utf-8').upper()


def raw2B(raw_data):
    """
    Convert raw binary data to hex representation, e.g. b'\xdf\x12g\xee\xdc\xba\x98v'-> b'DF1267EEDCBA9876'

    """
    return bytes(raw2str(raw_data), 'utf-8')


def B2raw(bin_data):
    """
    Convert hex representation to raw binary data, e.g. b'DF1267EEDCBA9876' -> b'\xdf\x12g\xee\xdc\xba\x98v'
    """
    return unhexlify(bin_data)


def xor(block1, block2):
    """
    XOR two blocks of data. Each block must be a hex representation of binary data, e.g. b'DF1267EEDCBA9876'
    """
    xored = ''.join(['{0:#0{1}x}'.format((i ^ j), 4)[2:] for i, j in zip(B2raw(block1), B2raw(block2))])
    return bytes(xored.upper(), 'utf-8')


def key_CV(key, kcv_length=6):
    """
    Get DES key check value. The key is binary hex e.g. b'DF1267EEDCBA9876'
    """
    cipher = DES3.new(B2raw(key), DES3.MODE_ECB)
    encrypted = raw2B(cipher.encrypt(B2raw(b'00000000000000000000000000000000')))

    return encrypted[:kcv_length]


def get_digits_from_string(cyphertext, length=4):
    """
    Extract PVV/CVV digits from the cyphertext (HEX-encoded string, e.g. 'EEFADCFFFBD7ADECAB9FBB')
    """
    digits = ''
   
    """
    The algorigthm is used for PVV and CVV calculation.

    1. The cyphertext is scanned from left to right. Decimal digits are
    selected during the scan until the needed number of decimal digits is found. 
    Each selected digit is placed from left to right according to the order
    of selection. If needed number of decimal digits is found (four in case of PVV, 
    three in case of CVV), those digits are the PVV or CVV.
    """
    for c in cyphertext:
        if len(digits) >= length:
            break
        try:
            int(c)
            digits += c
        except ValueError:
            continue
    
    """
    2. If, at the end of the first scan, less than four decimal digits
    have been selected, a second scan is performed from left to right.
    During the second scan, all decimal digits are skipped and only nondecimal
    digits can be processed. Nondecimal digits are converted to decimal
    digits by subtracting 10. The process proceeds until four digits of
    PVV are found.
    """
    if len(digits) < length:
        for c in cyphertext:
            if len(digits) >= length:
                break
    
            if (int(c, 16) - 10) >= 0:
                digits += str(int(c, 16) - 10)
    
    return digits


def get_visa_pvv(account_number, key_index, pin, PVK):
    """
    The algorithm generates a 4-digit PIN verification value (PVV) based on the transformed security parameter (TSP).
    
    For VISA PVV algorithms, the leftmost 11 digits of the TSP are the personal account number (PAN), 
    the leftmost 12th digit is a key table index to select the PVV generation key, and the rightmost 
    4 digits are the PIN. The key table index should have a value between 1 and 6, inclusive.
    """
    tsp = account_number[-12:-1] + key_index + pin
    if len(PVK) != 32:
        raise ValueError('Incorrect key length')

    left_key_cypher = DES3.new(PVK[:16], DES3.MODE_ECB)
    right_key_cypher = DES3.new(PVK[16:], DES3.MODE_ECB)

    encrypted_tsp = left_key_cypher.encrypt(right_key_cypher.decrypt((left_key_cypher.encrypt(B2raw(tsp)))))
    return bytes(get_digits_from_string(raw2str(encrypted_tsp)), 'utf-8')
