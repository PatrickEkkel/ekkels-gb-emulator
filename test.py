import opcodes
from bootrom import BootRom
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

    def test_LDHL16d(self):
        data = [0x21, 0xff,0x9f]
        self.create_testcontext(data)
        opcodes.LDHL16d(self.mmu, self.cpu)
        self.cpu.debugger.print_state(self.cpu.reg.GET_HL())
        assert self.cpu.reg.GET_HL() == 0x9fff

    def test_LDHL8A(self):
        data = []
        self.create_testcontext(data)
        bootrom = BootRom()
        self.mmu.set_bios(bootrom)
        self.cpu.reg.SET_AF(0x10ff)
        self.cpu.reg.SET_HL(0x9fff)
        opcodes.LDHL8A(self.mmu,self.cpu)
        self.cpu.debugger.print_state(self.cpu.reg.GET_HL())
        #assert True
        assert self.mmu.read(0x9fff) == 0x10

    def test_BIT7H(self):
        data = [0xCB,0x7c]
        self.create_testcontext(data)
        self.cpu.reg.SET_HL(0x8000)
        opcodes.CB(self.mmu,self.cpu)

        assert not self.cpu.reg.GET_ZERO_FLAG()

    def test_memory_init(self):
        data = []
        mmu = MMU()
        bootrom = BootRom()
        mmu.set_bios(bootrom)
        expected_result = 0xffff
        
        mmu.write(0x8001,0xffff)
        actual_result = mmu.read(0x8001)
        assert actual_result == expected_result

    def test_read_signed_byte(self):
        mmu = MMU()
        bootrom = BootRom()
        mmu.set_bios(bootrom)
        actual_result = mmu.read_s8(11)
        assert actual_result == -5

if __name__ == '__main__':
    unittest.main()