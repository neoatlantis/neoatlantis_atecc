#!/usr/bin/env python3
from enum import IntEnum, Enum

class ByteVariable:
    
    def __init__(self, buf, slice_start, slice_end, readonly=False):
        assert type(buf) == memoryview
        self._buffer = buf
        self._slice = (slice_start, slice_end)
        self._readonly = readonly

    @property
    def value(self):
        return bytearray(bytes(self._buffer[self._slice[0]:self._slice[1]]))

    @value.setter
    def value(self, v):
        if self._readonly:
            raise ValueError("Attempting to write to readonly address.")
        self._buffer[self._slice[0]:self._slice[1]] = v



class BytesManipulator:

    def __init__(self, view):
        assert type(view) == memoryview
        self.view = view
        self._setup_variables()

    def _setup_variables(self):
        """Any inheritance of this class must implement this method and set up
        its own variables based on the memoryview at self.view."""
        raise NotImplementedError("Must implement this method.")
