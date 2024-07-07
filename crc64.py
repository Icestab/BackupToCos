import crcmod


class CRC64:
    def __init__(self, file_path):
        self.file_path = file_path

    def calculate_crc64(self):
        crc64_ecma = crcmod.mkCrcFun(
            0x142F0E1EBA9EA3693, initCrc=0, xorOut=0xFFFFFFFFFFFFFFFF, rev=True
        )
        with open(self.file_path, "rb") as f:
            data = f.read()
        crc_value = str(crc64_ecma(data))
        return crc_value
