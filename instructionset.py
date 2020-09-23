import opcodes
import bitwise_functions

instructions = [{'m': 'XOR A'      , 'opcode': opcodes.XORn     , 'length': 1, 'cycles': 4       , 'register_options': {'A': 0xAF} },
                {'m': 'LD r nn'    , 'opcode': opcodes.LDn8d    , 'length': 2, 'cycles': 8       , 'register_options': {'C': 0x0E,'B': 0x06 } },
                {'m': 'JP nnnn'    , 'opcode': opcodes.JPnn     , 'length': 3, 'cycles': 16      , 'register_options': {'x': 0xC3 } },
                {'m': 'NOP'        , 'opcode': opcodes.NOP      , 'length': 1, 'cycles': 4       , 'register_options': {'x': 0x00 } },
                {'m': 'DEC r'      , 'opcode': opcodes.DECn     , 'length': 1, 'cycles': 4       , 'register_options': {'B': 0x05 } },
                {'m': 'LD rr nnnn' , 'opcode': opcodes.LDnn16d  , 'length': 3, 'cycles': 12      , 'register_options': {'HL': 0x21} }, 
                {'m': 'LDD (HL) A' , 'opcode': opcodes.LDDHL8A  , 'length': 1, 'cycles': 8       , 'register_options': {'x': 0x32 } },
                {'m': 'JRNZ nn'      , 'opcode': opcodes.JRNZn    , 'length': 2, 'cycles': [8, 12] , 'register_options': {'x': 0x20 } }, 
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
    elif len(operand) == 3:
        result = 'nnn'
        adressing_mode = 8

    elif len(operand) == 2:
        result = 'nn'
        adressing_mode = 8

    if adressing_mode == -1:
        return (result, operand, adressing_mode)
    else:
        return (result, int(operand, 16), adressing_mode)

def encode_one_byte_instruction(r, opcode, mnemonic_dict):
    result = mnemonic_dict[r[0]]['register_options']['x']
    return (result, None, None, 1)

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
    return (result, encoding_operand, first_operand, 2)



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
    return (result, second_operand, converted_value_operand, 3)


def handle_special_instruction(r, opcode, mnemonic_dict):
    result =  mnemonic_dict[r]['register_options']['x']
    return (result, None, None, 1)


def resolve_instruction(instruction, r, opcode,mnemonic_dict):
    encoded_instruction = None

    # check if this is 'special' instruction. 

    if r[0] == 'LDD':
        encoded_instruction = handle_special_instruction(instruction, opcode,mnemonic_dict)
    elif len(r) == 1:
        encoded_instruction = encode_one_byte_instruction(r, opcode,mnemonic_dict)
            
    elif len(r) == 2:
        encoded_instruction = encode_two_byte_instruction(r, opcode, mnemonic_dict)
      

    elif len(r) == 3:
        encoded_instruction = encode_three_byte_instruction(r, opcode, mnemonic_dict)
    return encoded_instruction


def is_label(instruction, r):
    return ':' in instruction and len(r) == 1

        
# very crude GB ASM to binary conversion, used to test small programs and CPU correctness
def create_bitstream(program):
    mnemonic_dict = create_mnemonic_dictionary()
    bitstream = []
    gc_labels = {}
    pc = 0x0100

    # index all the labels
    for instruction in program:
        r = instruction.split(' ')
        opcode = r[0]
        print(instruction)
        if is_label(instruction, r):
            gc_labels[instruction] = pc 
        # special case, instruction with label, meaning its an address so instructionlegnth is 2 bytes + 1 byte for the opcode
        elif ':' in instruction and len(r) > 1:
            pc += 3
        else:
            # get the length of the instruction 
            pc += len(r)
    
    # reset the pc counter
    pc = 0x0100
    for instruction in program:
        r = instruction.split(' ')
        converted_operand_value = None
        operand_value = None
        converter_register_operand = None
        opcode = r[0]
        if is_label(instruction, r):
            pass
            #bitstream.append(0x00)
            #pc += 1

        elif ':' in instruction and len(r) > 1:
            # identify label within mnemonic
            bc = 0
            for i in r:
                if ':' in i:
                    # lookup label in global label dictionary
                    address = gc_labels[i]
                    # there is different adressing modes for JP we need 16 bit, for JR we need 8 bit (signed)
                    if 'JRNZ' == r[0]:
                        # get the difference between the current pc and the label
                        dest =  (pc - address) * -1
                        print('blargh')
                        print(dest)
                        r[bc] =  str(dest) # encode_16bit_value(dest)
                    else:
                        r[bc] = encode_16bit_value(address)
                    
                    
                    encoded_instruction = resolve_instruction(instruction, r, opcode, mnemonic_dict)
                    decoded_instruction = encoded_instruction[0]
                    operand_value = encoded_instruction[2]
                    converted_operand_value = encoded_instruction[1]
                    break
                bc += 1
                    
        else:
           encoded_instruction = resolve_instruction(instruction, r, opcode, mnemonic_dict)
           decoded_instruction = encoded_instruction[0]
           operand_value = encoded_instruction[2]
           converted_operand_value = encoded_instruction[1]
        
        if not is_label(instruction, r):
            bitstream.append(decoded_instruction)
            
            if converted_operand_value:
                addressing_mode = operand_value[2]
                if addressing_mode == 16:
                    highbyte = bitwise_functions.get_highbyte(converted_operand_value)
                    lowbyte = bitwise_functions.get_lowbyte(converted_operand_value)
                    bitstream.append(lowbyte)
                    bitstream.append(highbyte)
                    pc += 2
                elif addressing_mode == 8:
                    bitstream.append(converted_operand_value)
                    pc += 1
        
     
    return bitstream


def create_instructionset():
    result = [None] * 255
    for i in instructions:
        for opcode in i['register_options'].values():
            #print(opcode)
            result[opcode] = i['opcode']
        #result[i['i']] = i['opcode']
    return result

