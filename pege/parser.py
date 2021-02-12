from instructionset import create_mnemonic_dictionary, create_cb_mnemonic_dictionary

OFFSET_REGISTERS = ['(C)','(HL)','(DE)']
REGISTERS_8B = ['A', 'B', 'C', 'D', 'E', 'F','H','L']
REGISTERS_16B = ['HL', 'DE', 'SP', 'BC']

SPECIAL_OPCODES = ['LDI','LDH']
def encode_8bit_value(value):
    if isinstance(value, str):
        value = int(value, 16)
        result =  "{:x}".format(value)
    else:
        result =  "{:x}".format(value)
    if len(result) == 1:
        result = "0{:x}".format(value)
    return result

def encode_16bit_value(value):
    if value:
        if isinstance(value, str):
            value = int(value, 16)
            result =  "{:x}".format(value)
        else:
            result =  "{:x}".format(value)

        #paddington
        if len(result) == 1:
            result = "000{:x}".format(value)
        elif len(result) == 2:
            result = "00{:x}".format(value)
        elif len(result) == 3:
            result = "0{:x}".format(value)
        return f'{result}'
    else:
        return None

class ParserError(Exception):
    pass

class Token:

    def __init__(self):
        self.label = None

    def get_label(self):
        return self.label.replace(':','')

class Label(Token):
    def __init__(self, label):
        self.label = label

class Opcode(Token):

    REGISTER_TRANSFER = 'rt'
    OFFSET_REGISTER_TRANSFER = 'ort'
    def __init__(self):
        self.mnemonic = ''
        self.label =  None
        self.register = None
        self.address = None
        self.addressing_mode = None

    def determine_adressing_mode(self):
        if self.address in REGISTERS_8B and self.register in REGISTERS_8B:
            self.addressing_mode = Opcode.REGISTER_TRANSFER
        elif self.register in OFFSET_REGISTERS and self.address in REGISTERS_8B:
            self.addressing_mode = Opcode.OFFSET_REGISTER_TRANSFER
        elif self.register in REGISTERS_8B and self.address in OFFSET_REGISTERS:
            self.addressing_mode = Opcode.OFFSET_REGISTER_TRANSFER
        elif self.register in REGISTERS_16B and self.address in REGISTERS_16B:
            self.addressing_mode = Opcode.OFFSET_REGISTER_TRANSFER
            

    def has_label(self):
        return self.label is not None

    def _print_register(self):
        result = ''
        if len(self.register) == 1 and self.register.isnumeric():
            result = 'b'
        if len(self.register) == 1 and (self.register in REGISTERS_8B or self.register in REGISTERS_16B):
            result = 'r'
        elif len(self.register) == 2:
            result = 'rr'
        elif len(self.register) == 3 and not 'H' in self.register:
            result = '(r)'
        elif len(self.register) == 4:
            result = '(rr)'
        return result

    def _print_address(self):
        result = ''
        # check if the the value is address or register
        if self.address in REGISTERS_8B:
            return 'r'
        elif self.address in REGISTERS_16B:
            return 'rr'
        elif self.address in OFFSET_REGISTERS:
            return '(rr)'
        else:
            pass
            if isinstance(self.address, int):
                # if address if of type int, it means it is a converted label 16 bit
                result = 'nnnn'
            elif len(self.address) == 4:
                result = 'nnnn'
            elif len(self.address) == 2:
                result = 'nn'
            elif len(self.address) == 3 and 'H' in self.address:
                result = 'nnH'
            elif len(self.address) == 1:
                result = 'nn'
            return result

    def get_mnemonic_label(self):
        # make exceptions for LDH
        if self.mnemonic == 'LDH':
            return f'LDH {self._print_address()} A'
        else:
            if self.register and self.address:
                return f'{self.mnemonic} {self._print_register()} {self._print_address()}'
            elif self.register:
                return f'{self.mnemonic} {self._print_register()}'
            elif self.address:
                return f'{self.mnemonic} {self._print_address()}'
            else:
                return f'{self.mnemonic}'

    def __str__(self):
        return self.get_mnemonic_label()

class Tokenizer:

    def __init__(self):
        pass


    def _is_label(self):
        # if first token contains : so it must be a label
        return ':' in self.tokens[0]
    def _get_label(self):
        for token in self.tokens:
            if ':' in token:
                return token

    def tokenize(self, line):
        self.tokens = line.split(' ')
        result = None

        if len(self.tokens) > 0:
            if self._is_label():
                result = Label(self._get_label())
            elif self._get_mnemonic() == 'LDD':
                result = Opcode()
                result.mnemonic = line
            elif self._get_mnemonic() == 'LDI':
                result = Opcode()
                result.mnemonic = line
            elif self._get_mnemonic() == 'LDH':
                result = Opcode()
                result.mnemonic = self._get_mnemonic()
                result.address = self._get_address()
            else:
                result = Opcode()
                result.mnemonic = self._get_mnemonic()
                result.label = self._get_label()
                result.register = self._get_register()
                result.address = self._get_address()
                #input(result.register)
                result.determine_adressing_mode()
                # determine, 8 bit or 16 bit value
                if result.address and result.address not in OFFSET_REGISTERS and result.address not in REGISTERS_16B:
                    if len(result.address) == 4:
                        result.address = encode_16bit_value(result.address)
                    elif len(result.address) == 2:
                        result.address = encode_8bit_value(result.address)

        return result

    def _get_mnemonic(self):
        return self.tokens[0]

    def _get_register(self):
        if len(self.tokens) > 1 and self.tokens[1] in REGISTERS_16B:
            return self.tokens[1]
        elif len(self.tokens) > 1 and len(self.tokens[1]) == 1:
            return self.tokens[1]
        elif len(self.tokens) > 1 and len(self.tokens[1]) == 3 and not 'H' in self.tokens[1]:
            return self.tokens[1]
        elif  len(self.tokens) > 1 and len(self.tokens[1]) == 4 and (self.tokens[1] in REGISTERS_16B or self.tokens[1] in REGISTERS_8B  or self.tokens[1] in OFFSET_REGISTERS):
            return self.tokens[1]
        else:
            return None

    def _get_address(self):
        # Make exception for LDH
        if self.tokens[0] == 'LDH':
            return self.tokens[1]
        else:
            if len(self.tokens) > 2:
                return self.tokens[2]
            elif len(self.tokens) > 1 and len(self.tokens[1]) == 4 and (self.tokens[1] not in REGISTERS_16B and self.tokens[1] not in REGISTERS_8B and self.tokens[1] not in OFFSET_REGISTERS):
                return self.tokens[1]
            elif len(self.tokens) > 1 and len(self.tokens[1]) == 3 and 'H' in self.tokens[1]:
                return self.tokens[1]
            elif len(self.tokens) > 1 and len(self.tokens[1]) == 2 and (self.tokens[1] not in REGISTERS_16B and self.tokens[1] not in REGISTERS_8B and self.tokens[1] not in OFFSET_REGISTERS):
                return self.tokens[1]
            else:
                return None


class GBA_ASM:
    def __init__(self):
        self.label_lookuptable = {}
        self.encoded_program = []
        self.instructions = create_mnemonic_dictionary()
        self.offset = 0x100
        self.program_counter = self.offset + 0x00


    def print_hex(self, opcode):
        return ("0x{:x}".format(opcode))


    def _preprocess(self, program):
        program_counter = 0x00
        for p in program:
            tokenizer = Tokenizer()
            opcode = tokenizer.tokenize(p)

            if isinstance(opcode, Label):
                #input('jup found label')
                current_address = self.offset + program_counter
                self.label_lookuptable[opcode.get_label()] = current_address + 2
                program_counter += 2
            else:
                program_counter += 1


    def _handle_opcode(self, opcode):
        opcode_meta = self.instructions.get(opcode.get_mnemonic_label())
        if not opcode_meta:
            raise ParserError(f' unknown opcode {opcode.get_mnemonic_label()}')

        else:
            # if we need to load two registers for example LD A B, concatinate
            # the operands
            if opcode.addressing_mode == Opcode.REGISTER_TRANSFER or opcode.addressing_mode == Opcode.OFFSET_REGISTER_TRANSFER:
                key = f'{opcode.register} {opcode.address}'
                self.encoded_program.append(opcode_meta['register_options'][key])
            elif opcode.register and not opcode.register.isnumeric():
                self.encoded_program.append(opcode_meta['register_options'][opcode.register])
            elif opcode.address and 'H' in opcode.address and len(opcode.address) == 3:
                # RST
                self.encoded_program.append(opcode_meta['register_options'][opcode.address])   
            elif opcode.address and opcode.address in REGISTERS_8B:
                self.encoded_program.append(opcode_meta['register_options'][opcode.address])     
            else:
                self.encoded_program.append(opcode_meta['register_options']['x'])
            if opcode.address:
                # does not support 8 bit adresses yet
                if len(opcode.address) == 4 and opcode.addressing_mode != Opcode.OFFSET_REGISTER_TRANSFER:
                    opcode.address = encode_16bit_value(opcode.address)
                    fb = opcode.address[2:4]
                    sb = opcode.address[0:2]
                    self.encoded_program.append(int(fb, 16))
                    self.encoded_program.append(int(sb, 16))
                elif len(opcode.address) == 2 and opcode.addressing_mode != Opcode.OFFSET_REGISTER_TRANSFER:
                    fb = opcode.address[0:2]
                    opcode.address = fb
                    self.encoded_program.append(int(fb, 16))
                elif str(opcode.address) == '0':
                    opcode.address = 0x0
                    self.encoded_program.append(0x0)

    def _handle_opcode_label(self, opcode):
        # the asm command contains label that needs to be translated
        # to an address
        label = opcode.get_label()

        address = self.label_lookuptable.get((opcode.get_label()))
        if address is None:
            raise ParserError(f'label {label} is not defined')
        else:
             # labels are always 16 bit addresses
             opcode.address = encode_16bit_value(address)
             opcode_meta = self.instructions[opcode.get_mnemonic_label()]
             encoded_opcode = opcode_meta['register_options']['x']
             # check if opcode needs a signed or an unsigned value

             # is it 8 bit signed?
             if opcode_meta['datatype'] == 'r8':
                 self.encoded_program.append(encoded_opcode)
                 result = address
                 if address > self.program_counter:
                     signed_address = address
                     # TODO: this is not working correctly
                     self.encoded_program.append(int(0x00))
                 else:
                     signed_address = ((self.program_counter) - address - self.offset) * -1
                     signed_address = address
                     #print('jump address goes back')
                     #input(signed_address)
                     self.encoded_program.append(signed_address)
             else:
                 self.encoded_program.append(encoded_opcode)
                 # split value in two 8 byte values and store
                 fb = opcode.address[2:4]
                 sb = opcode.address[0:2]
                 self.encoded_program.append(int(fb, 16))
                 self.encoded_program.append(int(sb, 16))

    def parse(self, program):
        normal_instructions = create_mnemonic_dictionary()
        cb_instructions = create_cb_mnemonic_dictionary()

        self._preprocess(program)
        for p in program: 
            if 'CB' in p:
                self.instructions = cb_instructions
                p = p.replace('CB ','')
                self.encoded_program.append(0xCB)
            else:
                self.instructions = normal_instructions

            tokenizer = Tokenizer()
            opcode = tokenizer.tokenize(p)
            address = None

            
            if isinstance(opcode, Opcode):
                if opcode.has_label():
                    self._handle_opcode_label(opcode)
                    opcode_meta = self.instructions[opcode.get_mnemonic_label()]
                    self.program_counter += opcode_meta['length']

                else:
                    opcode_meta = self.instructions[opcode.get_mnemonic_label()]
                    self._handle_opcode(opcode)
                    self.program_counter += opcode_meta['length']
            #self.program_counter += 1
        return self.encoded_program
