#!/usr/bin/env python

from binascii import hexlify

def raw2str(raw_data):
    """
    Convert raw binary data to string representation, e.g. b'\xdf\x12g\xee\xdc\xba\x98v'-> 'DF1267EEDCBA9876'
    """
    return hexlify(raw_data).decode('utf-8').upper()
