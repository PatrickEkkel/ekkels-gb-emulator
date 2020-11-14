class Debugger:

    def __init__(self, cpu):
        self.cpu = cpu
        self.show_registers = True
        self.show_opcodes = True
        self.show_cpu_flags = False
        self.show_program_counter = True
        self.step_instruction = False
        self.stop_at = 0x21b
        self.stop_at_opcode = None

    def format_hex(self, opcode):
        return ("0x{:x}".format(opcode))

    def print_opcode(self, opcode_description):
        if self.cpu.debug_opcode:
            print(opcode_description, end=' ')

    def print_register(self):
        if self.show_registers:
            AF = self.format_hex(self.cpu.reg.GET_AF())
            BC = self.format_hex(self.cpu.reg.GET_BC())
            DE = self.format_hex(self.cpu.reg.GET_DE())
            HL = self.format_hex(self.cpu.reg.GET_HL())
            print(f'AF: {AF}')
            print(f'BC: {BC}')
            print(f'DE: {DE}')
            print(f'HL: {HL}')
    def print_iv(self, value):
        if self.cpu.debug_opcode and self.show_opcodes:
            hex = self.format_hex(value)
            print(f'{hex} ',end=' ')

    def end(self):
        print('')

    def print_cpu_flags(self):
        if self.cpu.debug_opcode and self.show_cpu_flags:
            hex = self.format_hex(self.cpu.reg.GET_F())
            print(f'FLAGS-REG: {hex}')

    def print_state(self, data):
        hex = self.format_hex(data)
        hex_pc = self.format_hex(self.cpu.pc)
        if self.cpu.debug_opcode and self.show_program_counter:
            print(f'PC: {hex_pc} CPU: {hex}', end=' ')

    def debug(self, pc, opcode):
        if self.step_instruction or self.stop_at == pc:
            self.print_register()
            input('press enter to continue...')

        if self.stop_at_opcode == opcode:
            self.print_register()
            input('press enter to continue...')

        return