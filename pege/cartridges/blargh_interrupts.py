from cartridges.cartridge import Cartridge
class BlarghInterrupts(Cartridge):
    def __init__(self):
        super().__init__('cartridges/roms/interrupt_time.gb')