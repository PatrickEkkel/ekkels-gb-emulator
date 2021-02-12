from .mmu import MMU
from instructionset import opcode_descriptions
class Debugger:

    def __init__(self, cpu, mmu):
        self.cpu = cpu
        self.mmu = mmu
        self.show_registers = True
        self.show_stack = False
        self.show_vram = False
        self.show_opcodes = True
        self.show_cpu_flags = False
        self.show_program_counter = True
        self.step_instruction = False
        self.show_description = False
        self.stop_at = None
        self.stop_at_opcode = None #0xEF
        self.stop_and_step_at = None # 0x2824 # 0x29a8 #0x29B3
        self.exit_at_breakpoint = False


    def format_hex(self, opcode):
        return ("0x{:x}".format(opcode))

    def print_opcode(self, opcode_description):
        if self.show_opcodes:
            print(opcode_description, end=' ')

    def show_opcode_description(self,mnemonic):
        if self.show_description:
            opcode_description = opcode_descriptions.get(mnemonic)
            if opcode_description:
                print(opcode_description)

    def print_register(self):
        if self.show_registers:
            AF = self.format_hex(self.cpu.reg.GET_AF())
            BC = self.format_hex(self.cpu.reg.GET_BC())
            DE = self.format_hex(self.cpu.reg.GET_DE())
            HL = self.format_hex(self.cpu.reg.GET_HL())
            SP = self.format_hex(self.cpu.reg.GET_SP())
            print('\n')
            print(f'AF: {AF}')
            print(f'BC: {BC}')
            print(f'DE: {DE}')
            print(f'HL: {HL}')
            print(f'SP: {SP}')
    def print_stack(self):
        if self.show_stack:
            SP = self.cpu.reg.GET_SP()
            end_of_stack = 0xFFFF
            print('\n')
            
            i = SP
            while(i < end_of_stack):
                if self.mmu.read(i) != 0x00 or i == SP:
                    mem_address = "0x{:x}".format(i)
                    mem_value = "0x{:x}".format(self.mmu.read(i))
                    print(f' {mem_address}: {mem_value} ')
                i += 1
                
    def print_vram(self):
        if self.show_vram:
            start =  MMU.VRAM_START
            current = start
            end = MMU.VRAM_END
            if self.show_vram:
                while(current < end):
                    current += 1
                    value = self.mmu.read(current)
                    if value != 0x00:
                        address = current
                        print('address: ' + self.format_hex(address))
                        print('value: ' + self.format_hex(self.mmu.read(value)))

    def print_iv(self,value):
        if self.show_opcodes and self.show_opcodes:
            hex = self.format_hex(value)
            print(f' {hex} ',end=' ')

    def end(self):
        if self.show_opcodes:
            print('')

    def print_cpu_flags(self):
        if self.show_opcodes and self.show_cpu_flags:
            hex = self.format_hex(self.cpu.reg.GET_F())
            print(f'FLAGS-REG: {hex}')

    def print_state(self, data):
        hex = self.format_hex(data)
        hex_pc = self.format_hex(self.cpu.pc)
        if self.show_opcodes and self.show_program_counter:
            print(f'PC: {hex_pc} CPU: {hex}', end=' ')

    def debug(self, pc, opcode):
        if self.stop_and_step_at and pc == self.stop_and_step_at:
            self.step_instruction = True
            self.print_register()
            self.print_stack()
            self.print_vram()
            input('press enter to continue...')
            return True

        elif self.step_instruction or self.stop_at == pc:
            self.print_register()
            self.print_vram()
            self.print_stack()
            input('press enter to continue...')
            return True

        elif self.stop_at_opcode == opcode:
            self.print_register()
            input('press enter to continue...')
            return True
