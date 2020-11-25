from instructionset import create_mnemonic_dictionary


def encode_8bit_value(value):
    if isinstance(value, str):
        value = int(value, 16)
        result =  "{:x}".format(value)
    else:
        result =  "{:x}".format(value)
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

    def __init__(self):
        self.mnemonic = ''
        self.label =  None
        self.register = None
        self.address = None


    def has_label(self):
        return self.label is not None

    def _print_register(self):
        result = ''
        if len(self.register) == 1:
            result = 'r'
        elif len(self.register) == 2:
            result = 'rr'

        return result

    def _print_address(self):
        result = ''
        if isinstance(self.address, int):
            # if address if of type int, it means it is a converted label 16 bit
            result = 'nnnn'
        elif len(self.address) == 4:
            result = 'nnnn'
        elif len(self.address) == 2:
            result = 'nn'
        elif len(self.address) == 1:
            result = 'nn'
        return result

    def get_mnemonic_label(self):
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

            else:
                result = Opcode()
                result.mnemonic = self._get_mnemonic()
                result.label = self._get_label()
                result.register = self._get_register()
                result.address = self._get_address()
                # determine, 8 bit or 16 bit value

                if result.address:
                    if len(result.address) == 4:
                        result.address = encode_16bit_value(result.address)
                    elif len(result.address) == 2:
                        result.address = encode_8bit_value(result.address)

        return result

    def _get_mnemonic(self):
        return self.tokens[0]

    def _get_register(self):

        if len(self.tokens) > 1 and self.tokens[1] == 'HL':
            return self.tokens[1]
        elif len(self.tokens) > 1 and len(self.tokens[1]) == 1:
            return self.tokens[1]
        else:
            return None

    def _get_address(self):
        if len(self.tokens) > 2:
            return self.tokens[2]
        elif len(self.tokens) > 1 and len(self.tokens[1]) == 4:
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
            if opcode.register:
                self.encoded_program.append(opcode_meta['register_options'][opcode.register])
            else:
                self.encoded_program.append(opcode_meta['register_options']['x'])

            if opcode.address:
                # does not support 8 bit adresses yet
                if len(opcode.address) == 4:
                    opcode.address = encode_16bit_value(opcode.address)
                    fb = opcode.address[2:4]
                    sb = opcode.address[0:2]
                    self.encoded_program.append(int(fb, 16))
                    self.encoded_program.append(int(sb, 16))
                elif len(opcode.address) == 2:
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
                     print('Not implemented yet!')
                     self.encoded_program.append(int(0x00))
                 else:
                     signed_address = ((self.program_counter) - address - self.offset) * -1
                     self.encoded_program.append(signed_address)
             else:
                 self.encoded_program.append(encoded_opcode)
                 # split value in two 8 byte values and store
                 fb = opcode.address[2:4]
                 sb = opcode.address[0:2]
                 self.encoded_program.append(int(fb, 16))
                 self.encoded_program.append(int(sb, 16))

    def parse(self, program):
        instructions = create_mnemonic_dictionary()

        self._preprocess(program)
        for p in program:
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