import sys

class Coin(object):
    @classmethod
    def static_header_offset(cls, height):
        raise Exception('Not implemented')


class Wagerr(Coin):
    PRE_ZEROCOIN_BLOCKS = 1
    PRE_ZEROCOIN_HEADER_SIZE = 80
    ZEROCOIN_HEADER_SIZE = 112

    @classmethod
    def static_header_offset(cls, height):
        if height >= cls.PRE_ZEROCOIN_BLOCKS:
            return cls.PRE_ZEROCOIN_HEADER_SIZE * cls.PRE_ZEROCOIN_BLOCKS + cls.ZEROCOIN_HEADER_SIZE * (height - cls.PRE_ZEROCOIN_BLOCKS)
        return cls.PRE_ZEROCOIN_HEADER_SIZE * height

    def get_header_size(self, header: bytes):
        hex_to_int = lambda s: int.from_bytes(s, byteorder='little')
        if hex_to_int(header[0:4]) > 3:
            return self.ZEROCOIN_HEADER_SIZE
        return self.PRE_ZEROCOIN_HEADER_SIZE

    @classmethod
    def get_header_size_height(cls, height: int):
        if height in [1052605]: 
            return cls.PRE_ZEROCOIN_HEADER_SIZE
        return cls.ZEROCOIN_HEADER_SIZE if height >= cls.PRE_ZEROCOIN_BLOCKS  else cls.PRE_ZEROCOIN_HEADER_SIZE

    def check_header_size(self, header: bytes):
        size = self.get_header_size(header)
        if len(header) == self.PRE_ZEROCOIN_HEADER_SIZE:
            return True
        if len(header) == size:
            return True
        return False


class WagerrTestnet(Wagerr):
    PRE_ZEROCOIN_BLOCKS = 1
