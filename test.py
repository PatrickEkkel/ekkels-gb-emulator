import opcodes
from bootrom import BootRom
from emulator import CPU, MMU,Registers
from cartridges.testrom import TestRom
import unittest 



class OpcodeTests(unittest.TestCase):

    def print_hex(self, value):
        print("0x{:x}".format(value))

    def create_testcontext(self,data,disable_bootrom=True):
        self.mmu = MMU()
        if data:
            self.mmu.set_rom(TestRom(data))
        if disable_bootrom:
            self.mmu.disable_bootrom()
        
        self.cpu = CPU(self.mmu)

    def create_rom_testcontext(self, opcode_under_test, disable_bootrom=True):
        # rom header from a known working ROM that we can use to test various opcodes on
        self.rom_header = [
        0x0,0xc3,0x50,0x1,0xce,0xed,0x66,0x66,0xcc,0xd,0x0,0xb,0x3,0x73,0x0,
        0x83,0x0,0xc,0x0,0xd,0x0,0x8,0x11,0x1f,0x88,0x89,0x0,0xe,0xdc,0xcc,
        0x6e,0xe6,0xdd,0xdd,0xd9,0x99,0xbb,0xbb,0x67,0x63,0x6e,0xe,0xec,0xcc,
        0xdd,0xdc,0x99,0x9f,0xbb,0xb9,0x33,0x3e,0x4d,0x41,0x52,0x49,0x4f,0x4c,
        0x41,0x4e,0x44,0x32,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x3,0x4,0x2,0x1,
        0x1,0x0,0x13,0xe0,0xf9]
    
        self.mmu = MMU()
        no_op_length = 0x100 - len(opcode_under_test)
        no_op = [0x00] * no_op_length

        data = opcode_under_test + no_op
        data = data + self.rom_header
        self.address_space = data
        self.mmu.set_rom(TestRom(data))

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
        data = [0x00,0xCD,0x00,0x01]
        self.create_rom_testcontext(data)
        self.cpu.pc = 1
        self.cpu.reg.SET_SP(0xFFFF)
        opcodes.CALLnn(self.mmu, self.cpu)
        # simulate the step method by added 1 to the pc (just like in the emulation)
        self.cpu.pc += 1
        
        assert self.cpu.pc == 0x100
        assert self.cpu.reg.GET_SP() == 0xFFFE
        assert self.mmu.read(0xFFFE) == 0x02
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
        data = [0xE0,0x10]
        self.create_testcontext(data)
        self.cpu.reg.SET_AF(0x10ff)
        self.cpu.reg.SET_HL(0x9fff)
        expected_address = 0xFF00 + 0x10
        opcodes.LDHnA(self.mmu,self.cpu)
        assert self.mmu.read(expected_address) == 0x10

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
        assert self.mmu.read(expected_address) == 0xab

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


    def test_A_register(self):
        data  = []
        self.create_testcontext(data)
        self.cpu.reg.SET_A(0x80)
        self.cpu.reg.SET_CARRY()
        print('blurpking')
        self.print_hex(self.cpu.reg.GET_A())
        #assert self.cpu.reg.GET_A() == 0x80

    def test_RLA(self):
        data =[0x17]
        
        self.create_testcontext(data)
        # test rotate bit with carry set and value 0x80
        # expecting bit left rotate from 1000 0000 to 0000 0001 which is non zero and msb is put in carry flag
        self.cpu.reg.SET_CARRY()
        self.cpu.reg.SET_A(0x80)
        
        opcodes.RLA(self.mmu, self.cpu)
        self.cpu.debugger.end()
        assert self.cpu.reg.GET_CARRY()
        assert not self.cpu.reg.GET_ZERO()
        assert self.cpu.reg.GET_CARRY() == 0x01
        
        # carry is cleared, value is set to 0x80, expecting ZERO bit SET
        self.cpu.reg.CLEAR_CARRY()
        self.cpu.reg.SET_A(0x80)
        opcodes.RLA(self.mmu, self.cpu)
        self.cpu.debugger.end()
        assert self.cpu.reg.GET_ZERO()
        assert self.cpu.reg.GET_CARRY()
        assert self.cpu.reg.GET_A() == 0x00
        # carry bit is cleared, zero bit is cleared, putting in value 0x40
        # rotation should go from 0100 0000 to 1000 0000

        self.cpu.reg.CLEAR_CARRY()
        self.cpu.reg.CLEAR_ZERO()
        self.cpu.reg.SET_A(0x40)
        opcodes.RLA(self.mmu, self.cpu)
        self.cpu.debugger.end()
        assert not self.cpu.reg.GET_CARRY()
        #assert not self.cpu.reg.GET_ZERO()
        #assert self.cpu.reg.GET_A() == 0x80
      

        self.cpu.reg.SET_CARRY()
        self.cpu.reg.CLEAR_ZERO()
        self.cpu.reg.SET_A(0x00)
        opcodes.RLA(self.mmu, self.cpu)
        self.cpu.debugger.end()
        assert not self.cpu.reg.GET_ZERO()
        assert not self.cpu.reg.GET_CARRY()
        print(self.cpu.reg.GET_A())
        print(self.cpu.reg.GET_A())
        assert self.cpu.reg.GET_A() == 0x01

    def test_RLC(self):
        data =[0xCB,0x11]
        
        self.create_testcontext(data)
        # test rotate bit with carry set and value 0x80
        # expecting bit left rotate from 1000 0000 to 0000 0001 which is non zero and msb is put in carry flag
        self.cpu.reg.SET_CARRY()
        self.cpu.reg.SET_C(0x80)
        
        opcodes.RLC(self.mmu, self.cpu)
        self.cpu.debugger.end()
        assert self.cpu.reg.GET_CARRY()
        assert not self.cpu.reg.GET_ZERO()
        assert self.cpu.reg.GET_C() == 0x01
        #self.print_hex(self.cpu.reg.GET_C())
        
        # carry is cleared, value is set to 0x80, expecting ZERO bit SET
        self.cpu.reg.CLEAR_CARRY()
        self.cpu.reg.SET_C(0x80)
        opcodes.RLC(self.mmu, self.cpu)
        self.cpu.debugger.end()
        assert self.cpu.reg.GET_ZERO()
        assert self.cpu.reg.GET_CARRY()
        assert self.cpu.reg.GET_C() == 0x00
        # carry bit is cleared, zero bit is cleared, putting in value 0x40
        # rotation should go from 0100 0000 to 1000 0000

        self.cpu.reg.CLEAR_CARRY()
        self.cpu.reg.CLEAR_ZERO()
        self.cpu.reg.SET_C(0x40)
        opcodes.RLC(self.mmu, self.cpu)
        self.cpu.debugger.end()
        assert not self.cpu.reg.GET_CARRY()
        assert not self.cpu.reg.GET_ZERO()
        assert self.cpu.reg.GET_C() == 0x80
      

        self.cpu.reg.SET_CARRY()
        self.cpu.reg.CLEAR_ZERO()
        self.cpu.reg.SET_C(0x00)
        opcodes.RLC(self.mmu, self.cpu)
        self.cpu.debugger.end()
        assert not self.cpu.reg.GET_ZERO()
        assert not self.cpu.reg.GET_CARRY()
        assert self.cpu.reg.GET_C() == 0x01
        
        

    def test_LDAn(self):
        data = [0x1A]
        self.create_rom_testcontext(data)
        self.cpu.reg.SET_DE(0x104)
        opcodes.LDAn(self.mmu, self.cpu)
        A = self.cpu.reg.GET_A()
        self.print_hex(A)
        assert A == 0xce
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

    def test_the_test(self):
        data = [0x10]
        self.create_rom_testcontext(data)
        assert self.mmu.read(0x100 + 1) == 0xc3


    def test_registers(self):
        data = [0x00]
        self.create_testcontext(data)
        self.cpu.reg.SET_BC(0x0000)
        self.cpu.reg.SET_C(0x20)
        self.cpu.reg.SET_B(0xAB)
        assert self.cpu.reg.GET_C() == 0x20
        assert self.cpu.reg.GET_B() == 0xAB
        assert self.cpu.reg.GET_BC() == 0xAB20

        pass
        
if __name__ == '__main__':
    unittest.main()