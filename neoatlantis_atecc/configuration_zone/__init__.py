#!/usr/bin/env python3
from enum import IntEnum, Enum

from ._base import *
from .slot_config import *
from .key_config import *
from .use_lock import *
from .i2c_address import *



class ConfigurationZone(BytesManipulator):

    def __init__(self, initialvalue):
        assert type(initialvalue) == bytearray and len(initialvalue) == 128
        buf = bytearray(bytes(initialvalue))
        BytesManipulator.__init__(self, memoryview(buf))

    def _setup_variables(self):
        self.i2c_address = I2CAddress(self.view, 16, 16+1)
        self.use_lock = UseLock(self.view, 68, 68+1)
        self.slot_config = SlotConfig(self.view[20:51+1])
        self.key_config = KeyConfig(self.view[96:127+1])




