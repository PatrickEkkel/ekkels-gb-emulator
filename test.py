import opcodes
from emulator import CPU, MMU
import unittest 



class OpcodeTests(unittest.TestCase):
    def create_testcontext(self,data):
        self.mmu = MMU()
        self.mmu.set_rom(data)
        self.mmu.disable_bootrom()
        self.cpu = CPU(self.mmu)

    def test_LDSP16d(self):
        data = [0x31,0xf9,0xff]
        self.create_testcontext(data)
        opcodes.LDSP16d(self.mmu, self.cpu)
        assert self.cpu.reg.GET_SP() == 0xfff9

    def test_LDHL8A(self):
        data = []
        self.create_testcontext(data)
        opcodes.LDHL8A(self.mmu,self.cpu)
        assert True
if __name__ == '__main__':
    unittest.main()