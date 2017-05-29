pynblock
========
 
A payment card industry crypto library - PIN blocks, card/PIN verification values calculation etc

Usage: 
 >>> from pynblock.tools import *
 >>> check_key_parity(bytes.fromhex('FA9F90D49CB27B7D14A3FA9CCCFF6CB7'))
 True
 >>> modify_key_parity(bytes.fromhex('32743CD2823EF937A865A18A8A3A1657'))
 b'3t<\xd2\x82?\xf99\xa9e\xa3\x8b\x8b:\x17Y'
