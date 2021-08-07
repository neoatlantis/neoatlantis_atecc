#!/usr/bin/env python3
from enum import IntEnum

class ByteVariable(IntEnum):
    
    def __init__(self, buf, default):
        assert type(buf) == memoryview
        self._value = default
        self._buffer = buf
        IntEnum.__init__(self)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v.value
        self._buffer = self._value



class BytesManipulator:

    def __init__(self, buf):
        self.buffer = buf
        self.view = memoryview(self.buffer)

        self._setup_variables()

    def _setup_variables(self):
        """Any inheritance of this class must implement this method and set up
        its own variables based on the memoryview at self.view."""
        raise NotImplementedError("Must implement this method.")



if __name__ == "__main__":
    
    class TestV(ByteVariable):
        
        A = 1
        B = 2

    vb = bytesarray([0,0,0,0])
    vbv = memoryview(vb)
    v = TestV(vbv[3])
    
