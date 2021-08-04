#!/usr/bin/env python3

from ..crc16 import crc16

def read_param(param, length1=None, length2=None):
    print(type(param))
    assert type(param) in [bytearray, bytes, list, int]
    if type(param) == int:
        param = bytearray([param])
    if type(param) == list:
        param = bytearray(param)
    if type(param) == bytes:
        param = bytearray(param)
    if length1 != None:
        if length2 == None:
            assert len(param) == length1
        else:
            assert length1 <= len(param) <= length2
    return param





class COMMAND_PACKET:

    def __init__(self, opcode, param1, param2, data=b''):
        self._opcode = read_param(opcode, 1)
        self._param1 = read_param(param1, 1)
        self._param2 = read_param(param2, 1, 2)
        self._data = read_param(data)

        self._debug = True

    def __bytes__(self):
        """Returns security command packet over i2c.
        :param byte opcode: The command Opcode
        :param byte param_1: The first parameter
        :param byte param_2: The second parameter, can be two bytes.
        :param byte param_3 data: Optional remaining input data.
        """
        # assembling command packet
        command_packet = bytearray(8 + len(self._data))
        # word address
        command_packet[0] = 0x03
        # i/o group: count
        command_packet[1] = len(command_packet) - 1  # count
        # security command packets
        command_packet[2] = self._opcode
        command_packet[3] = self._param_1
        command_packet[4] = self._param_2 & 0xFF
        command_packet[5] = self._param_2 >> 8
        for i, cmd in enumerate(self._data):
            command_packet[6 + i] = cmd
        if self._debug:
            print("Command Packet Sz: ", len(command_packet))
            print("\tSending:", [hex(i) for i in command_packet])
        # Checksum, CRC16 verification
        crc = crc16(command_packet[1:-2])
        command_packet[-1] = crc >> 8
        command_packet[-2] = crc & 0xFF

        return bytes(command_packet)
