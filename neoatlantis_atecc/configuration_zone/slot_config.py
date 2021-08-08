#!/usr/bin/env python3

from enum import Enum, IntEnum
from ._base import *
from ._function_proxy import FunctionProxy


class WriteConfig:
    
    class FLAGS(Enum):
        WRITE_ALWAYS      = FunctionProxy(lambda a,b,c,d: a==b==c==d==0)
        WRITE_PUBINVALID  = FunctionProxy(lambda a,b,c,d: a==b==c==0 and d == 1)
        WRITE_NEVER       = FunctionProxy(lambda a,b,c,d: (a==b==0 and c == 1) or (a==1 and b==0))
        WRITE_ENCRYPT     = FunctionProxy(lambda a,b,c,d: b==1)

        DERIVEKEY_ROLL_WITHOUT_MAC    = FunctionProxy(lambda a,b,c,d: a==d==0 and c==1)
        DERIVEKEY_ROLL_WITH_MAC       = FunctionProxy(lambda a,b,c,d: a==c==1 and d==0)
        DERIVEKEY_CREATE_WITHOUT_MAC  = FunctionProxy(lambda a,b,c,d: c==d==1 and a==0)
        DERIVEKEY_CREATE_WITH_MAC     = FunctionProxy(lambda a,b,c,d: a==c==d==1)
        DERIVEKEY_FORBIDDEN           = FunctionProxy(lambda a,b,c,d: c==0)

        GENKEY_ALLOWED     = FunctionProxy(lambda a,b,c,d: c==1)
        GENKEY_FORBIDDEN   = FunctionProxy(lambda a,b,c,d: c==0)

        PRIVWRITE_ALLOWED     = FunctionProxy(lambda a,b,c,d: b==1)
        PRIVWRITE_FORBIDDEN   = FunctionProxy(lambda a,b,c,d: b==0)

    @staticmethod
    def parseflags(value):
        value = value >> 12
        a,b,c,d = \
            (value & 0b1000) and 1 or 0, \
            (value & 0b0100) and 1 or 0, \
            (value & 0b0010) and 1 or 0, \
            (value & 0b0001) and 1 or 0
        ret = []
        for each in SlotWritePermission.FLAGS:
            if each.value(a,b,c,d): ret.append(each)
        return ret

    @staticmethod
    def getvalue(*flags):
        flags = list(flags)
        assert (
            set([e.name.split("_")[0] for e in flags]) ==\
            set(["WRITE", "DERIVEKEY", "GENKEY", "PRIVWRITE"])
        ), "SlotWritePermission must be set with flags out of 4 groups."

        ra, rb, rc, rd = tuple([f.value for f in flags])
        found = None 
        for bruteforce in range(0,16):
            a,b,c,d = \
                (bruteforce & 0b1000) and 1 or 0, \
                (bruteforce & 0b0100) and 1 or 0, \
                (bruteforce & 0b0010) and 1 or 0, \
                (bruteforce & 0b0001) and 1 or 0

            if ra(a,b,c,d) and rb(a,b,c,d) and rc(a,b,c,d) and rd(a,b,c,d):
                found = bruteforce
                break

        if None == found:
            raise ValueError(
                "Invalid combination for WriteConfig: " + 
                ", ".join([e.name for e in flags])
            )

        return found << 12





class SingleSlotConfig(ByteVariable):

    class FLAGS(IntEnum):
        NO_MAC          = 0b00010000
        LIMITED_USE     = 0b00100000
        ENCRYPT_READ    = 0b01000000
        IS_SECRET       = 0b10000000

    def __init__(self, buf, start):
        ByteVariable.__init__(self, buf, start, start+2, readonly=False)


    @property
    def flags(self):
        val = self.value[0] | (self.value[1] << 8)
        ret = []
        for e in self.FLAGS:
            if val & e.value:
                ret.append(e)
        return ret, SlotWritePermission.parseflags(val)
    
    @value.setter
    def value(self, read_key, write_key, *flags):
        flags = list(flags)
        assert 0 <= read_key <= 15
        assert 0 <= write_key <= 15
        write_config_flags = []
        slot_flags = []
        for e in flags:
            if type(e) == self.FLAGS:
                slot_flags.append(e)
            if type(e) == WriteConfig.FLAGS:
                write_config_flags.append(e)
        assert set([e.name.split("_")[0] for e in write_config_flags]) ==\
            set(["WRITE", "PRIVWRITE", "GENKEY", "DERIVEKEY"])

        write_config_value = WriteConfig.getvalue(*write_config_flags)
        slot_value = 0x00
        for e in slot_flags:
            slot_value |= e.value
        readkey_value = read_key & 0b1111
        writekey_value = (write_key & 0b1111) << 8
        
        ByteVariable.value =\
            write_config_value | slot_value | readkey_value | writekey_value







class SlotConfig(BytesManipulator):

    def __init__(self, view):
        assert len(view) == 32
        BytesManipulator.__init__(self, view)

    def _setup_variables(self):
        for i in range(0, 16):
            setattr(
                self,
                "slot%d" % i,
                SingleSlotConfig(self.view, start=i*2)
            )



if __name__ == "__main__":
    """    
        WRITE_ALWAYS      = lambda a,b,c,d: a==b==c==d==0
        WRITE_PUBINVALID  = lambda a,b,c,d: a==b==c==0 and d == 1
        WRITE_NEVER       = lambda a,b,c,d: (a==b==0 and c == 1) or (a==1 and b==0)
        WRITE_ENCRYPT     = lambda a,b,c,d: b==1

        DERIVEKEY_ROLL_WITHOUT_MAC    = lambda a,b,c,d: a==d==0 and c==1
        DERIVEKEY_ROLL_WITH_MAC       = lambda a,b,c,d: a==c==1 and d==0
        DERIVEKEY_CREATE_WITHOUT_MAC  = lambda a,b,c,d: c==d==1 and a==0
        DERIVEKEY_CREATE_WITH_MAC     = lambda a,b,c,d: a==c==d==1
        DERIVEKEY_FORBIDDEN           = lambda a,b,c,d: c==0

        GENKEY_ALLOWED     = lambda a,b,c,d: c==1
        GENKEY_FORBIDDEN   = lambda a,b,c,d: c==0

        PRIVWRITE_ALLOWED     = lambda a,b,c,d: b==1
        PRIVWRITE_FORBIDDEN   = lambda a,b,c,d: b==0
    """
    sample_config  = bytearray.fromhex("""
                    20 20 20 20  20 20 20 20 20 c0 00 55
        00 83 20 87 20 87 20 87  2f 87 2f 8f 8f 9f 8f af
        20 20 20 20""")
    slotconfigbuffer = memoryview(sample_config)

    slotconfig = SlotConfig(slotconfigbuffer)
    slot0 = slotconfig.slot0

    print("slot0", slot0.flags)
