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
