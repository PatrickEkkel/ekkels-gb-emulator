import opcodes
from bootrom import BootRom
from emulator import CPU, MMU,Registers
import unittest 



class OpcodeTests(unittest.TestCase):


    def print_hex(self, value):
        print("0x{:x}".format(value))

    def create_testcontext(self,data,disable_bootrom=True):
        self.mmu = MMU()
        if data:
            self.mmu.set_rom(data)
        if disable_bootrom:
            self.mmu.disable_bootrom()
        
        self.cpu = CPU(self.mmu)

    def test_LDSP16d(self):
        data = [0x31,0xf9,0xff]
        self.create_testcontext(data)
        opcodes.LDSP16d(self.mmu, self.cpu)
        assert self.cpu.reg.GET_SP() == 0xfff9

    def test_LDnn16d(self):
        data = [0x21, 0xff,0x9f]
        self.create_testcontext(data)
        opcodes.LDnn16d(self.mmu, self.cpu)
        self.cpu.debugger.print_state(self.cpu.reg.GET_HL())
        assert self.cpu.reg.GET_HL() == 0x9fff

    def test_CALLnn(self):
        
        assert False
    def test_LDDHL8A(self):
        data = []
        self.create_testcontext(data)
        bootrom = BootRom()
        self.mmu.set_bios(bootrom)
        self.cpu.reg.SET_AF(0x10ff)
        self.cpu.reg.SET_HL(0x9fff)
        opcodes.LDDHL8A(self.mmu,self.cpu)
        self.cpu.debugger.print_state(self.cpu.reg.GET_HL())
        #assert True
        assert self.mmu.read(0x9fff) == 0x10
        assert self.cpu.reg.GET_HL() == 0x9ffe

    def test_LDHL8A(self):
        data = []
        self.create_testcontext(data)
        bootrom = BootRom()
        self.mmu.set_bios(bootrom)
        self.cpu.reg.SET_AF(0x10ff)
        self.cpu.reg.SET_HL(0x9fff)
        opcodes.LDHnA(self.mmu,self.cpu)
        self.cpu.debugger.print_state(self.cpu.reg.GET_HL())
        #assert True
        assert self.mmu.read(0x9fff) == 0x10

    def test_LDHnA(self):
        data = [0xE0,0x78]
        self.create_testcontext(data)
        self.cpu.reg.SET_A(0xBA)
        assert True


    def test_BIT7H(self):
        data = [0xCB,0x7c]
        self.create_testcontext(data)
        self.cpu.reg.SET_HL(0x8000)
        opcodes.CB(self.mmu,self.cpu)

        assert not self.cpu.reg.GET_ZERO()
    def test_LDn8d_C(self):
        data = [0x0E,0x11]
        self.create_testcontext(data)
        opcodes.LDn8d(self.mmu, self.cpu)
        assert self.cpu.reg.GET_C() == 0x11

    def test_LDn8d_A(self):
        data = [0x3E,0x11]
        self.create_testcontext(data)
        opcodes.LDn8d(self.mmu, self.cpu)
        assert self.cpu.reg.GET_A() == 0x11
    

    def test_AF_register(self):
        data = []
        self.create_testcontext(data)
        self.cpu.reg.SET_AF(0xffff)
        assert self.cpu.reg.GET_AF() == 0xffff
        self.cpu.reg.SET_A(0x15)
        assert self.cpu.reg.GET_AF() == 0x15ff
        assert self.cpu.reg.GET_A() ==  0x15
        assert self.cpu.reg.GET_F() == 0xff
    

    def test_LDCA(self):
        self.create_testcontext(None,disable_bootrom=False)
        bootrom = BootRom()
        self.mmu.set_bios(bootrom)
        self.cpu.reg.SET_C(0x11)
        self.cpu.reg.SET_AF(0xabcd)
        opcodes.LDCA(self.mmu, self.cpu)
        expected_address = 0xFF00 + 0x11
        print(expected_address) 
        # TODO: this instruction writes to an I/O register, i have not implemented anything yet regarding to I/O
        assert self.mmu.read(expected_address) == 0x000

    def test_memory_init(self):
        data = []
        mmu = MMU()
        bootrom = BootRom()
        mmu.set_bios(bootrom)
        expected_result = 0xffff
        
        mmu.write(0x8001,0xffff)
        actual_result = mmu.read(0x8001)
        assert actual_result == expected_result

    def test_INCn(self):
        data = [0x0C]
        self.create_testcontext(data)
        self.cpu.reg.SET_C(0xEE)
        opcodes.INCn(self.mmu, self.cpu)
        C = self.cpu.reg.GET_C()
        assert C == 0xEF
        

    def test_flags_register(self):
        register = Registers()

        # flip the flag register and check if it is all working
        register.SET_ZERO()
        assert register.GET_ZERO() == True
        register.CLEAR_ZERO()
        assert register.GET_ZERO() == False
        register.SET_SUBSTRACT()
        assert register.GET_SUBSTRACT() == True
        register.CLEAR_SUBSTRACT()
        assert register.GET_SUBSTRACT() == False
        register.SET_HALF_CARRY()
        assert register.GET_HALF_CARRY() == True
        register.CLEAR_HALF_CARRY()
        assert register.GET_HALF_CARRY() == False
        register.SET_CARRY()
        assert register.GET_CARRY() == True
        register.CLEAR_CARRY()
        assert register.GET_CARRY() == False


        # do a few combinations of flags and see if it behaves correct

        register.SET_ZERO()
        register.SET_CARRY()
        register.SET_HALF_CARRY()
        register.SET_SUBSTRACT()

        assert register.GET_F() == 0xf0
        register.CLEAR_ZERO()
        assert register.GET_F() == 0x70
        register.CLEAR_CARRY() 
        assert register.GET_F() == 0x60
        register.CLEAR_HALF_CARRY()
        assert register.GET_F() == 0x40
        register.CLEAR_SUBSTRACT()
        assert register.GET_F() == 0x00

    def test_read_signed_byte(self):
        mmu = MMU()
        bootrom = BootRom()
        mmu.set_bios(bootrom)
        actual_result = mmu.read_s8(11)
        assert actual_result == -5

if __name__ == '__main__':
    unittest.main()