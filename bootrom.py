import sh, os, logging
from array import array
from config import logger



class BootRom:
    
    def __init__(self):
       
        bootrom_path = 'boot/dmg_boot.bin'
        self.data = array('B')
        with open(bootrom_path, 'rb') as bootrom:
            self.data.fromfile(bootrom, 256)
        logger.debug('Gameboy BootROM loaded')


