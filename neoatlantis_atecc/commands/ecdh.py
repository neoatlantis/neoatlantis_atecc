#!/usr/bin/env python3

import enum
from ._command import COMMAND_PACKET

class ECDH(COMMAND_PACKET):

    class SOURCE_KEY(enum.IntEnum):
        EEPROM  = 0b00000000
        TEMPKEY = 0b00000001

    class OUTPUT_ENCRYPTION(enum.IntEnum):
        CLEAR            = 0b00000000
        FORCE_ENCRYPTION = 0b00000010

    class RESULT_TARGET(enum.IntEnum):
        COMPATIBILITY    = 0b00000000
        EEPROM           = 0b00000100
        TEMPKEY          = 0b00001000
        OUTPUT_BUFFER    = 0b00001100

    def __init__(
        self,
        source_key=SOURCE_KEY.TEMPKEY,
        output_encryption=OUTPUT_ENCRYPTION.CLEAR,
        result_target=RESULT_TARGET.TEMPKEY,
        keyid=None,
        data=b'',
    ):

        assert len(data) == 64, "Missing public key."
        if source_key == self.SOURCE_KEY.EEPROM:
            assert keyid != None

        mode = source_key | output_encryption | result_target
        param2 = keyid if keyid != None else 0x0000

        if result_target == self.RESULT_TARGET.OUTPUT_BUFFER:
            resp_size = 64
        else:
            resp_size = 1


        COMMAND_PACKET.__init__(self,
            opcode=0x43,
            param1=mode,
            param2=param2,
            data=data,

            resp_size=resp_size
        )
