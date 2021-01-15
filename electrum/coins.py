import sys

class Coin(object):
    @classmethod
    def static_header_offset(cls, height):
        raise Exception('Not implemented')


class Wagerr(Coin):
    PRE_ZEROCOIN_BLOCKS = 1
    PRE_ZEROCOIN_HEADER_SIZE = 80
    ZEROCOIN_HEADER_SIZE = 112
    HEADER_V7_BLOCKS = 1501000
    HEADER_V7_SIZE = 80


    @classmethod
    def static_header_offset(cls, height):
        if height >= cls.HEADER_V7_BLOCKS:
            return cls.PRE_ZEROCOIN_HEADER_SIZE * cls.PRE_ZEROCOIN_BLOCKS + cls.ZEROCOIN_HEADER_SIZE * (cls.HEADER_V7_BLOCKS - cls.PRE_ZEROCOIN_BLOCKS) + cls.HEADER_V7_SIZE * (height - cls.HEADER_V7_BLOCKS)
        elif height >= cls.PRE_ZEROCOIN_BLOCKS:
            return cls.PRE_ZEROCOIN_HEADER_SIZE * cls.PRE_ZEROCOIN_BLOCKS + cls.ZEROCOIN_HEADER_SIZE * (height - cls.PRE_ZEROCOIN_BLOCKS)
        return cls.PRE_ZEROCOIN_HEADER_SIZE * height

    def get_header_size(self, header: bytes):
        hex_to_int = lambda s: int.from_bytes(s, byteorder='little')
        if hex_to_int(header[0:4]) > 3 and hex_to_int(header[0:4]) < 7: # 7 is header version after fork at block 1501000, size if V7 is 80
            return self.ZEROCOIN_HEADER_SIZE
        return self.PRE_ZEROCOIN_HEADER_SIZE

    @classmethod
    def get_header_size_height(cls, height: int):
        if height >= cls.PRE_ZEROCOIN_BLOCKS and height < cls.HEADER_V7_BLOCKS:
            return cls.ZEROCOIN_HEADER_SIZE
        else:
            return cls.PRE_ZEROCOIN_HEADER_SIZE
        

    def check_header_size(self, header: bytes):
        size = self.get_header_size(header)
        if len(header) == self.PRE_ZEROCOIN_HEADER_SIZE:
            return True
        if len(header) == size:
            return True
        return False


class WagerrTestnet(Wagerr):
    PRE_ZEROCOIN_BLOCKS = 1
