#!/usr/bin/env python3
from enum import IntEnum

class ByteVariable:
    
    def __init__(self, buf, slice_start, slice_end):
        assert type(buf) == memoryview
        self._buffer = buf
        self._slice = (slice_start, slice_end)

    @property
    def value(self):
        return bytearray(bytes(self._buffer[self._slice[0]:self._slice[1]]))

    @value.setter
    def value(self, v):
        self._buffer[self._slice[0]:self._slice[1]] = v



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

    vb = bytearray([0,0,0,0])
    vbv = memoryview(vb)
    v = TestV(vbv, 3, 4)
    
    v.value = b'\x10'
    print(vb)
