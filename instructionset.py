import opcodes
import bitwise_functions

instructions = [{'m': 'XOR A'      , 'opcode': opcodes.XORn     ,'length': 1, 'cycles': 4 , 'register_options': {'A': 0xAF} },
                {'m': 'LD r nn'    , 'opcode': opcodes.LDn8d    ,'length': 2, 'cycles': 8 , 'register_options': {'C': 0x0E,'B': 0x06 } },
                {'m': 'JP nnnn'    , 'opcode': opcodes.JPnn     ,'length': 3, 'cycles': 16, 'register_options': {'x': 0xC3 } },
                {'m': 'NOP'        , 'opcode': opcodes.NOP      ,'length': 1, 'cycles': 4 , 'register_options': {'x': 0x00 } },
                {'m': 'DEC r'      , 'opcode': opcodes.DECn     ,'length': 1, 'cycles': 4 , 'register_options': {'B': 0x05 } },
                {'m': 'LD rr nnnn' , 'opcode': opcodes.LDnn16d  ,'length': 3, 'cycles': 12, 'register_options': {'HL': 0x21} },  
               ]



def create_mnemonic_dictionary():
    result = {}
    for instruction in instructions:
        result[instruction['m']] = instruction
    
    return result

def _convert_operand(operand):
    result = operand
    adressing_mode = None
    # if the operand is 4 characters long it must be a 16 bit address
    if len(operand) == 4:
        result = 'nnnn'
        adressing_mode = 16
    elif len(operand) == 1:
        result = 'r'
        adressing_mode = -1
    elif len(operand) == 2 and ('H' in operand or 'L' in operand):
        result = 'rr'
        adressing_mode = -1
    elif len(operand) == 2:
        result = 'nn'
        adressing_mode = 8

    if adressing_mode == -1:
        return (result, operand, adressing_mode)
    else:
        return (result, int(operand, 16), adressing_mode)


def encode_two_byte_instruction(r, opcode, mnemonic_dict):
    operand = r[1]
    first_operand = _convert_operand(operand)
    normalized_operand = first_operand[0]
    encoding_operand = first_operand[1]
    normalized_instruction = f'{opcode} {normalized_operand}'
    # operand is an address or value, so its not important and we we can lookup the opcode without translating the address to opcode
    if first_operand[2] != -1:
        result = mnemonic_dict[normalized_instruction]['register_options']['x']
    else:
        result = mnemonic_dict[normalized_instruction]['register_options'][operand]
    return (result, encoding_operand, first_operand)



def encode_three_byte_instruction(r, opcode, mnemonic_dict):
    operand_1 = r[1]
    operand_2 = r[2]

    converted_value_operand = _convert_operand(operand_2)
    converter_register_operand = _convert_operand(operand_1)
    normalized_operand = converted_value_operand[0]
    second_operand = converted_value_operand[1]
    first_operand = converter_register_operand[0]
    normalized_instruction = f'{opcode} {first_operand} {normalized_operand}'
    #opcode_index = mnemonic_dict[normalized_instruction]['register_options'][operand_1]
    #result = mnemonic_dict[normalized_instruction]['i'][opcode_index]
    if converter_register_operand[2] != -1:
        result = mnemonic_dict[normalized_instruction]['register_options']['x']
    else:
        result = mnemonic_dict[normalized_instruction]['register_options'][operand_1]
    return (result, second_operand, converted_value_operand)


        
# very crude GB ASM to binary conversion, used to test small programs and CPU correctness
def create_bitstream(program):
    mnemonic_dict = create_mnemonic_dictionary()
    bitstream = []
    for instruction in program:
        r = instruction.split(' ')
        converted_operand_value = None
        operand_value = None
        converter_register_operand = None
        opcode = r[0]
        if len(r) == 1:
            decoded_instruction = mnemonic_dict[instruction]['register_options']['x']
            
        elif len(r) == 2:
            encoded_instruction = encode_two_byte_instruction(r, opcode, mnemonic_dict)
            converted_operand_value = encoded_instruction[1]
            operand_value = encoded_instruction[2]
            decoded_instruction = encoded_instruction[0]

        elif len(r) == 3:

            encoded_instruction = encode_three_byte_instruction(r, opcode, mnemonic_dict)
            converted_operand_value = encoded_instruction[1]
            operand_value = encoded_instruction[2]
            decoded_instruction = encoded_instruction[0]
        
        bitstream.append(decoded_instruction)
        if converted_operand_value:
            addressing_mode = operand_value[2]
            if addressing_mode == 16:
                highbyte = bitwise_functions.get_highbyte(converted_operand_value)
                lowbyte = bitwise_functions.get_lowbyte(converted_operand_value)
                bitstream.append(lowbyte)
                bitstream.append(highbyte)
            elif addressing_mode == 8:
                bitstream.append(converted_operand_value)
    return bitstream


def create_instructionset():
    result = [None] * 255
    for i in instructions:
        for opcode in i['register_options'].values():
            result[opcode] = i['opcode']
        #result[i['i']] = i['opcode']
    return result

