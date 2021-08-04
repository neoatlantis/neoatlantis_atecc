def crc16(data, length=None):
    if length is None:
        length = len(data)
    if not data or not length:
        return 0
    polynom = 0x8005
    crc = 0x0
    for b in data:
        for shift in range(8):
            data_bit = 0
            if b & (1 << shift):
                data_bit = 1
            crc_bit = (crc >> 15) & 0x1
            crc <<= 1
            crc &= 0xFFFF
            if data_bit != crc_bit:
                crc ^= polynom
                crc &= 0xFFFF
    return crc & 0xFFFF
