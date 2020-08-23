import sh, os, logging
import cartridges.mbc as mbc
from cartridges.mbc import MBC1
from array import array
from config import logger

class Cartridge:
    
    def __init__(self, path):
        self.data = array('B')
        size = os.path.getsize(path)
        
        with open(path, 'rb') as bootrom:
            self.data.fromfile(bootrom, size)
            logger.debug('Gameboy cartridge loaded')
        self._create_mbc()


    def _create_mbc(self):
        ctype = self.get_cartridgetype()
        if ctype == mbc.MBC1BATTERYRAM:
            logger.debug('MBC1+BATTERY+RAM created')
            return MBC1(self.get_ramsize())

    def get_cartridgetype(self):
        return self.data[0x0147]
    
    def get_ramsize(self):
        return self.data[0x0149]


    def print_cartridge_info(self):
        print('Cartridge type: ' + str(self.get_cartridgetype()))
        print('RAM size: type: ' + str(self.get_ramsize()))

