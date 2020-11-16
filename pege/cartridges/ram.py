from array import array
class RAM:
    def __init__(self, size, cartridge_flag):
        self.cartridge_flag = cartridge_flag
        self.size = size
        self.data = array('B')