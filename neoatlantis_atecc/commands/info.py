#!/usr/bin/env python3
import enum
from ._command import COMMAND_PACKET

class INFO(COMMAND_PACKET):

    class MODE(enum.IntEnum):
        REVISION            = 0x00
        KEYVALID            = 0x01
        STATE               = 0x02
        GPIO                = 0x03
        VOLATILE_KEY_PERMIT = 0x04

    def __init__(self, mode=MODE.REVISION, param=0x00):

        COMMAND_PACKET.__init__(self,
            opcode=0x30,
            param1=int(mode),
            param2=param,
            data=b""
        )
