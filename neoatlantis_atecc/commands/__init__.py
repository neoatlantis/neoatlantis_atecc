#!/usr/bin/env python3

import enum
from ._command import COMMAND_PACKET

from .selftest import SELFTEST
from .info import INFO
from .read import READ


class AES(COMMAND_PACKET):

    def __init__(self, mode, keyid, input):

        COMMAND_PACKET.__init__(self,
            opcode=0x51,
            param1=mode,
            param2=keyid,
            data=input
        )



