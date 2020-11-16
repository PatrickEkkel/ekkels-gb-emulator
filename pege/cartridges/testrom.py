from cartridges.cartridge import Cartridge
class TestRom(Cartridge):
    def __init__(self,data):
        super().__init__(None)
        self.data = data