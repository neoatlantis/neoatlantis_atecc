#!/usr/bin/env python3

import os
import board
import busio
from neoatlantis_atecc import ATECC, _WAKE_CLK_FREQ
from neoatlantis_atecc.configuration_zone import ConfigurationZone



# Initialize the i2c bus
i2c = busio.I2C(board.SCL, board.SDA, frequency=_WAKE_CLK_FREQ)

atecc = ATECC(i2c)
print(atecc.serial_number)

print(atecc.version())

print("\nstate")
print(atecc.state())

#print("\nkey 8 valid")
#print(atecc.keyvalid(8))

print("-" * 20 + " Read Configuration Zone " + "-" * 20)
config_value = atecc.read_config()
print("Current config value:")
print(config_value.hex())
config_zone = ConfigurationZone(bytearray(config_value))
slot_config = config_zone.slot_config
print("Slot config value:")
print(bytes(slot_config.view).hex())

for i in range(0, 16):
    slotiflags = getattr(slot_config, "slot%d" % i).flags
    print("Slot %d\t" % i, ", ".join([e.name for e in slotiflags[0] + slotiflags[1]]))



