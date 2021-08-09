#!/usr/bin/env python3

from enum import Enum, IntEnum
from ._base import *



class SingleKeyConfig(ByteVariable):

    class FLAGS(IntEnum):
        PRIVATE = 0b00000001    # contains ECC private key
        PUBINFO = 0b00000010    # see manual 2.2.11
        KEYTYPE_P256_ECC     = 0b00010000
        KEYTYPE_AES          = 0b00011000
        KEYTYPE_SHA_OR_OTHER = 0b00011100
        LOCKABLE             = 0b00100000
        REQUIRE_RANDOM       = 0b01000000
        REQUIRE_AUTH         = 0b10000000
        PERSISTENT_DISABLE   = 0b1000000000000

    def __init__(self, buf, start):
        ByteVariable.__init__(self, buf, start, start+2, readonly=False)

    @property
    def flags(self):
        val = self.value[0] | (self.value[1] << 8)
        ret = []
        for e in self.FLAGS:
            if val & e.value:
                ret.append(e)
        return ret

    @property
    def auth_key(self):
        return self.value[1] & 0b1111

    @property
    def X509id(self):
        return (self.value[1] & 0b11000000) >> 6

    @auth_key.setter
    def auth_key(self, value):
        self.value[1] &= (0b11110000 | (value & 0b1111))

    @X509id.setter
    def X509id(self, value):
        self.value[1] &= (0b00111111 | ((value & 0b11) << 6))
    
    @flags.setter
    def flags(self, flags):
        flags = list(flags)
        key_flags = []
        for e in flags:
            if type(e) == self.FLAGS:
                key_flags.append(e)
            else:
                raise Exception("Invalid flag for keyconfig.")

        if len([e.name for e in key_flags if e.name.startswith("KEYTYPE_")) > 1:
            raise Exception("KEYTYPE must be set to only one flag.")

        key_value = 0x00
        for e in key_flags:
            key_value |= e.value
        authkey_value = (self.auth_key & 0b1111) << 8
        X509id_value = (self.X509id & 0b11) << 14
        
        # a 16-bit integer
        newvalue = key_value | authkey_value | X509id_value

        assert newvalue & 0b00011100 != 0 and newvalue & (1<<13) != 0, \
            "Invalid key config value. Flags missing?"

        self.value = bytearray([keyvalue & 0xFF, (keyvalue >> 8) & 0xFF])




class KeyConfig(BytesManipulator):

    def __init__(self, view):
        assert len(view) == 32
        BytesManipulator.__init__(self, view)

    def _setup_variables(self):
        for i in range(0, 16):
            setattr(
                self,
                "key%d" % i,
                SingleKeyConfig(self.view, start=i*2)
            )



if __name__ == "__main__":
    pass
