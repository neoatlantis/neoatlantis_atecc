#!/usr/bin/env python3
from enum import IntEnum, Enum

from ._base import *
from .slot_config import *



class ConfigurationZone(BytesManipulator):

    def __init__(self, initialvalue):
        assert type(initialvalue) == bytearray and len(initialvalue) == 128
        buf = bytearray(bytes(initialvalue))
        BytesManipulator.__init__(self, memoryview(buf))

    def _setup_variables(self):
        self.slot_config = SlotConfig(self.view[20:51+1])





