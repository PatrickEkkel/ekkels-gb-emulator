from instructionset import create_mnemonic_dictionary

def encode_16bit_value(value):
    if value:
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
                        print('8 bit value nog niet ondersteund')

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
        self.instructions = create_mnemonic_dictionary()
        self.program_counter = 0x00
        self.offset = 0x100


    def print_hex(self, opcode):
        return ("0x{:x}".format(opcode))


    def _preprocess(self, program):
        program_counter = 0x00
        for p in program:
            tokenizer = Tokenizer()
            opcode = tokenizer.tokenize(p)

            if isinstance(opcode, Label):
                #print(self.print_hex())
                program_counter += 2
                current_address = self.offset + program_counter
                self.label_lookuptable[opcode.get_label()] = current_address
            else:
                program_counter += 1

    def parse(self, program):
        instructions = create_mnemonic_dictionary()
        encoded_program = []
        self._preprocess(program)
        for p in program:
            tokenizer = Tokenizer()
            opcode = tokenizer.tokenize(p)
            address = None
            if isinstance(opcode, Opcode):
                if opcode.has_label():
                   # the asm command contains label that needs to be translated
                   # to an address
                   label = opcode.get_label()
                   address = self.label_lookuptable.get((opcode.get_label()))
                   if address is None:
                       raise ParserError(f'label {label} is not defined')
                   else:
                        # labels are always 16 bit addresses
                        opcode.address = encode_16bit_value(address)
                        print(opcode.get_mnemonic_label())
                        encoded_opcode = self.instructions[opcode.get_mnemonic_label()]['register_options']['x']
                        hex_opcode = self.print_hex(encoded_opcode)
                        encoded_program.append(encoded_opcode)
                        # split value in two 8 byte values and store
                        fb = opcode.address[2:4]
                        sb = opcode.address[0:2]
                        encoded_program.append(int(fb, 16))
                        encoded_program.append(int(sb, 16))
                        #encoded_program.append(address)
                else:
                    opcode_meta = self.instructions.get(opcode.get_mnemonic_label())
                    if not opcode_meta:
                        raise ParserError(f' unknown opcode {opcode.get_mnemonic_label()}')

                    else:
                        if opcode.register:
                            encoded_program.append(opcode_meta['register_options'][opcode.register])
                        else:
                            encoded_program.append(opcode_meta['register_options']['x'])
                        #if opcode.address:
                        #    encoded_program.append(int(opcode.address, 16))
        return encoded_program