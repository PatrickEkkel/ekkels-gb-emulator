from cartridges.ram import RAM
MBC1BATTERYRAM = 0x03

RAM8K = 0x02

class MBC:
    def __init__(self):
        pass


class MBC1(MBC):

    def __init__(self, ramsize):

        self._create_ram(ramsize)
    def _create_ram(self, ramsize):
        if ramsize == RAM8K:
            return RAM(1024 * 8, ramsize)
                    

