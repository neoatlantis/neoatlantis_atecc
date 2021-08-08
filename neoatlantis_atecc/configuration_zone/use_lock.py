#!/usr/bin/env python3
from ._base import *

class UseLock(ByteVariable):

    @property
    def use_lock_enable(self):
        return self.value[0] & 0b1111 == 0x0A

    @use_lock_enable.setter
    def use_lock_enable(self, value):
        if value:
            self.value[0] &= 0xFA
        else:
            self.value[0] &= 0xF0

    @property
    def use_lock_key(self):
        return self.value[0] >> 4

    @use_lock_key.setter
    def use_lock_key(self, value):
        self.value[0] &= (value << 4) | 0x0F
