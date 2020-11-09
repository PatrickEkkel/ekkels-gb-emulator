import opcodes
import bitwise_functions

instructions = [{'m': 'XOR r'      , 'datatype': '', 'opcode': opcodes.XORn     , 'length': 1, 'cycles': 4       , 'register_options': {'A': 0xAF} },
                {'m': 'LD r nn'    , 'datatype': '', 'opcode': opcodes.LDn8d    , 'length': 2, 'cycles': 8       , 'register_options': {'C': 0x0E,'B': 0x06 } },
                {'m': 'JP nnnn'    , 'datatype': '', 'opcode': opcodes.JPnn     , 'length': 3, 'cycles': 16      , 'register_options': {'x': 0xC3 } },
                {'m': 'NOP'        , 'datatype': '', 'opcode': opcodes.NOP      , 'length': 1, 'cycles': 4       , 'register_options': {'x': 0x00 } },
                {'m': 'DEC r'      , 'datatype': '', 'opcode': opcodes.DECn     , 'length': 1, 'cycles': 4       , 'register_options': {'B': 0x05 } },
                {'m': 'LD rr nnnn' , 'datatype': '', 'opcode': opcodes.LDnn16d  , 'length': 3, 'cycles': 12      , 'register_options': {'HL': 0x21} },
                {'m': 'LDD (HL-) A', 'datatype': '', 'opcode': opcodes.LDDHL8A  , 'length': 1, 'cycles': 8       , 'register_options': {'x': 0x32 } },
                {'m': 'JRNZ nnnn'  , 'datatype': 'a8', 'opcode': opcodes.JRNZn    , 'length': 2, 'cycles': [8, 12] , 'register_options': {'x': 0x20 } },
               ]



def get_instruction_by_mnemonic(mnemonic):
    instructions = create_mnemonic_dictionary()

    for i in instructions:
        if i['m'] == mnemonic:
            return i

def create_mnemonic_dictionary():
    result = {}
    for instruction in instructions:
        result[instruction['m']] = instruction

    return result


def encode_8bit_value(value):
    result =  "{:x}".format(value)

    return result

def encode_16bit_value(value):
    result =  "{:x}".format(value)
    #paddington
    if len(result) == 3:
        result = "0{:x}".format(value)
    elif len(result) == 2:
        result = "00{:x}".format(value)

    return result


def handle_special_instruction(r, opcode, mnemonic_dict):
    result =  mnemonic_dict[r]['register_options']['x']
    return (result, None, None, 1)


def create_bitstream(test_program):
    return []


def create_instructionset():
    result = [None] * 255
    for i in instructions:
        for opcode in i['register_options'].values():
            #print(opcode)
            result[opcode] = i['opcode']
        #result[i['i']] = i['opcode']
    return result
