from components.cpu import opcodes
from bootrom import BootRom
from components.cpu.cpu import CPU,Registers
from components.mmu import MMU
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

    def test_AF_register(self):
        data = []
        self.create_testcontext(data)
        self.cpu.reg.SET_AF(0xffff)
        assert self.cpu.reg.GET_AF() == 0xffff
        self.cpu.reg.SET_A(0x15)
        assert self.cpu.reg.GET_AF() == 0x15ff
        assert self.cpu.reg.GET_A() ==  0x15
        assert self.cpu.reg.GET_F() == 0xff


    def test_memory_init(self):
        data = []
        mmu = MMU()
        bootrom = BootRom()
        mmu.set_bios(bootrom)
        expected_result = 0xffff

        mmu.write(0x8001,0xffff)
        actual_result = mmu.read(0x8001)
        assert actual_result == expected_result


    def test_wrap_around_register(self):
        data = [0x05]
        self.create_testcontext(data)
        self.cpu.reg.SET_BC(0x0010)
        opcodes.DECn(self.mmu, self.cpu)
        self.print_hex(self.cpu.reg.GET_BC())
        assert True

    def test_LDAn(self):
        data = [0x1A]
        self.create_rom_testcontext(data)
        self.cpu.reg.SET_DE(0x104)
        opcodes.LDAn(self.mmu, self.cpu)
        A = self.cpu.reg.GET_A()
        assert A == 0xce

    def test_zero_plus_halfcarry_register(self):
        data = []
        self.create_testcontext(data)
        self.cpu.reg.SET_AF(0x0080)
        self.cpu.reg.CLEAR_ZERO()
        self.cpu.reg.SET_HALF_CARRY()
        self.cpu.reg.SET_SUBSTRACT()
        assert self.cpu.reg.GET_AF() == 0x0060

    def test_zero_flags_register(self):
        data1 = [0xAF,0x00]
        self.create_testcontext(data1)
        self.cpu.reg.SET_AF(0x01B0)

        opcodes.XORn(self.mmu, self.cpu)
        #self.cpu.reg.SET_ZERO()
        self.print_hex(self.cpu.reg.GET_AF())
        assert self.cpu.reg.GET_AF() == 0x0080

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




if __name__ == '__main__':
    unittest.main()
