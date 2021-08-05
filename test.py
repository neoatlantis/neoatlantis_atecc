#!/usr/bin/env python3

import board
import busio
from neoatlantis_atecc import ATECC, _WAKE_CLK_FREQ

# Initialize the i2c bus
i2c = busio.I2C(board.SCL, board.SDA, frequency=_WAKE_CLK_FREQ)

atecc = ATECC(i2c)
print(atecc.serial_number)

print(atecc.version())

print("\nstate")
print(atecc.state())

print("\nkey 8 valid")
print(atecc.keyvalid(8))

print("all config")
print(atecc.read_config())
