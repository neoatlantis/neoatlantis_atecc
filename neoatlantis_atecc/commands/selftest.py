#!/usr/bin/env python3
import enum
from ._command import COMMAND_PACKET

class SELFTEST(COMMAND_PACKET):

    class MODE(enum.IntEnum):
        ALL             = 0x3F
        RNG_DRGB        = 0b00000001
        ECDSA_VERIFY    = 0b00000010
        ECDSA_SIGN      = 0b00000100
        ECDH            = 0b00001000
        AES             = 0b00010000
        SHA             = 0b00100000

    def __init__(self, mode=MODE.ALL):

        COMMAND_PACKET.__init__(self,
            opcode=0x77,
            param1=int(mode),
            param2=b"\x00\x00",
            data=b"",

            resp_size=1
        )
