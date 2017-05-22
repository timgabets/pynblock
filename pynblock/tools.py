#!/usr/bin/env python

import sys
from binascii import hexlify, unhexlify
from Crypto.Cipher import DES, DES3


def str2bytes(data):
    """
    """
    if sys.version_info[0] == 3:
        return bytes(data, 'utf-8')
    else:
        return bytes(data)


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


def get_visa_cvv(account_number, exp_date, service_code, CVK):
    """
    """
    if len(CVK) != 32:
        raise ValueError('Incorrect key length')
        
    tsp = exp_date + service_code + b'000000000'
    des_cipher = DES.new(B2raw(CVK[:16]))
    des3_cipher = DES3.new(B2raw(CVK), DES3.MODE_ECB)
        
    block1 = xor(raw2B(des_cipher.encrypt(B2raw(account_number))), tsp)
    block2 = des3_cipher.encrypt(B2raw(block1))

    return get_digits_from_string(raw2str(block2), 3)


def get_clear_pin(pinblock, account_number):
    """
    Calculate the clear PIN from provided PIN block and account_number, which is the 12 right-most digits of card account number, excluding check digit
    """
    raw_pinblock = bytes.fromhex(pinblock.decode('utf-8'))
    raw_acct_num = bytes.fromhex((b'0000' + account_number).decode('utf-8'))
        
    pin_str = xor(raw2B(raw_pinblock), raw2B(raw_acct_num)).decode('utf-8')
    pin_length = int(pin_str[:2], 16)
    
    if pin_length >= 4 and pin_length < 9:
        pin = pin_str[2:2+pin_length]            
        try:
            int(pin)
        except ValueError:
            raise ValueError('PIN contains non-numeric characters')
        return bytes(pin, 'utf-8')
    else:
        raise ValueError('Incorrect PIN length: {}'.format(pin_length))


def get_pinblock(__PIN, __PAN):
    """
    """
    PIN = str(__PIN)
    PAN = str(__PAN)

    if not PIN or not PAN:
        return None

    block1 = '0' + str(len(PIN)) + str(PIN)
    while len(block1) < 16:
        block1 += 'F'
    block2 = '0000' + PAN[-13:-1]

    try:
        raw_message = bytes.fromhex(block1)
        raw_key = bytes.fromhex(block2)
    except ValueError:
        return ''

    result = ''.join(["{0:#0{1}x}".format((i ^ j), 4)[2:] for i, j in zip(raw_message, raw_key)])
    return result


def parityOf(int_type):
    """
    Calculates the parity of an integer, returning 0 if there are an even number of set bits, and -1 if there are an odd number. 
    """
    parity = 0
    while (int_type):
        parity = ~parity
        int_type = int_type & (int_type - 1)
    return(parity)


def check_key_parity(key):
    """
    Perform the parity check for a given key.

    Returns False if the key fails the parity check
    Returns True if the key is fine
    """
    for byte in key:
        if parityOf(int(byte)) == -1:
            return False
    return True


def modify_key_parity(key):
    """
    The prior use of the function is to return the parity-validated key.

    The incoming key is expected to be hex data binary representation, e.g. b'E7A3C8B1'
    """
    validated_key = b''
    for byte in key:
        if parityOf(int(byte)) == -1:
            byte_candidate = int(byte) + 1 
            while parityOf(byte_candidate) == -1:
                byte_candidate = divmod(byte_candidate + 1, 256)[1]
            validated_key += bytes([byte_candidate])

        else:
            validated_key += bytes([byte])
    return validated_key


