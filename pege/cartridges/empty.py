from cartridges.cartridge import Cartridge

class Empty(Cartridge):
    def __init__(self):
        super().__init__(None)
