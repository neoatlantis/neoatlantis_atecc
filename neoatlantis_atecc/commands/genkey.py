#!/usr/bin/env python3

import enum
from ._command import COMMAND_PACKET

class GENKEY(COMMAND_PACKET):

    class MODE(enum.IntEnum):
        GENERATE        = 0b00000100
        DERIVE_PUBLIC   = 0b00000000
        # TODO more bits in mode

    def __init__(self, mode=MODE.GENERATE, keyid=0xFFFF, data=b''):

        COMMAND_PACKET.__init__(self,
            opcode=0x40,
            param1=mode,
            param2=keyid,
            data=data,

            resp_size=64
        )
