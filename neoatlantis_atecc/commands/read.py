#!/usr/bin/env python3

import enum
from ._command import COMMAND_PACKET

class READ(COMMAND_PACKET):

    class LENGTH(enum.IntEnum):
        LENGTH_4  = 0
        LENGTH_32 = 0b10000000

    class ZONE(enum.IntEnum):
        CONFIG  = 0
        OTP     = 1
        DATA    = 2

    def __init__(
        self,
        length=LENGTH.LENGTH_32, zone=ZONE.CONFIG,
        block=0, slot=None, offset=0
    ):
        if zone == ZONE.CONFIG or zone == ZONE.OTP:
            assert slot == None, "Zone 'config' and 'otp' have no slots."
            if zone == ZONE.CONFIG:
                assert 0 <= block <= 3, "Invalid block id for zone 'config'."
            if zone == ZONE.OTP:
                assert 0 <= block <= 1, "Invlaid block id for zone 'data'."
            param2 = block << 3 # (10.5.1 zone encoding)

        if zone == DATA:
            assert 0 <= slot <= 15, "Invalid slot id."
            if slot <= 7:
                assert 0 <= block <= 1, "Invalid block id for slot %d" % slot
            elif slot <= 8:
                assert 0 <= block <= 12, "Invalid block id for slot %d" % slot
            elif slot <= 15:
                assert 0 <= block <= 2, "Invalid block id for slot %d" % slot
            param2 = (block << 8) | ((slot & 0b1111) << 3)


        param1 = int(zone) | int(length)
        param2 = param2 | (offset & 0b111)

        COMMAND_PACKET.__init__(self,
            opcode=0x02,
            param1=param1,
            param2=param2,
            data=b"",

            resp_size=(32 if length == LENGTH.LENGTH_32 else 4)
        )
