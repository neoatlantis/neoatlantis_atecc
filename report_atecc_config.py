#!/usr/bin/env python3

import os
import board
import busio
from neoatlantis_atecc import ATECC, _WAKE_CLK_FREQ
from neoatlantis_atecc.configuration_zone import ConfigurationZone

def show_hex(bytestring):
    h = bytestring.hex()
    chunksize = 32 
    spaced = lambda l: " ".join([l[i:i+2] for i in range(0, len(l), 2)])
    chunks = [ spaced(h[i:i+chunksize]) for i in range(0, len(h), chunksize) ]
    return "\n".join(chunks)



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
#config_value  = bytearray.fromhex("""0123bcae00005000455b669beec04500c0005500837181018371c10183718371 8371c171010183718371c1718371837183718371000000ff00020002ffffffff    00000000ffffffffffffffffffffffffffffffff00000000ffff000000000000        13003c0013003c0013003c0013003c003c003c0013003c0013003c0013003300""") # nitrokey sample
print("Current config value:")
print(show_hex(bytes(config_value)))
config_zone = ConfigurationZone(bytearray(config_value))
slot_config = config_zone.slot_config
print("\n")

print("I2C ADDRESS:", config_zone.i2c_address.value)
print("USE LOCK STATUS:", "Enabled=%s" % config_zone.use_lock.use_lock_enable, "Key=%d" % config_zone.use_lock.use_lock_key)

print("Slot config value:")
print(bytes(slot_config.view).hex())

for i in range(0, 16):
    sloti = getattr(slot_config, "slot%d" % i)
    slotiflags = sloti.flags
    print(
        "Slot %d\t" % i,
        "READ_KEY=%d" % sloti.read_key,
        "WRITEKEY=%d" % sloti.write_key,
        ", ".join([e.name for e in slotiflags[0] + slotiflags[1]])
    )



