import opcodes

instructions = [{'m': 'XOR A'     , 'opcode': opcodes.XORn     ,'length': 1, 'cycles': 4 , 'i': 0xAF },
                {'m': 'DEC B'     , 'opcode': opcodes.DECn     ,'length': 1, 'cycles': 4 , 'i': 0x05 },
                {'m': 'LD C d8'   , 'opcode': opcodes.LDn8d    ,'length': 2, 'cycles': 8 , 'i': 0x0E },
                {'m': 'LD HL d16' , 'opcode': opcodes.LDnn16d  ,'length': 3, 'cycles': 12, 'i': 0x21 },  
               ]

# very crude GB ASM to binary conversion, used to test small programs and CPU correctness
def create_bitstream(program):
    pass


def create_instructionset():
    result = [None] * 255
    for i in instructions:
        result[i['i']] = i['opcode']
    return result

