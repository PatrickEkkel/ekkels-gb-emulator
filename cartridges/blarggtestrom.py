from cartridges.cartridge import Cartridge
class BlarrgCPUTest(Cartridge):
    def __init__(self):
        super().__init__('cartridges/roms/cpu_instrs.gb')