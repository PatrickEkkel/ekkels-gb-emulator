from memorymap import *
from .component import Component

class JoyPad(Component):
    
    JOYPAD_DIRECTIONS = 0xCF
    JOYPAD_BUTTONS = 0xEF
    P15 = 0x20
    P14 = 0x10

    def __init__(self, mmu):
        super().__init__(mmu)
        self.value = 0x00

    def read(self, address):
        # P15
        if self.value == JoyPad.P15:
            return JoyPad.JOYPAD_BUTTONS
        elif self.value == JoyPad.P14:
            return JoyPad.JOYPAD_DIRECTIONS
        # P14

    def write(self, address, value):
        # filter out everything except bit 4 and 5
        self.value = value & 0x30

        # check if P15 is set

        if self.value & JoyPad.P15:
            self.value = JoyPad.P15
            # return button nibble on read
        # check if P14 is set
        elif self.value & JoyPad.P14:
            self.value = JoyPad.P14

            # return  joypad nibble on read
        
        
    def is_in_range(self, address):
        return JP_REGISTER == address
            
