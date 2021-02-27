from components.cpu import  opcodes
from components.cpu.opcode_dsl import OpcodeContext
from components.cpu.opcode_dsl_new import NewOpcodeContext
import bitwise_functions

opcode_descriptions = {'LDH r nn': 'LDH A,(n) = put memory address $FF00+n into A'}

cb_instructions =  [{'m': 'CB', 'datatype': '', 'opcode': opcodes.CB, 'length': 1, 'cycles': 4, 'jump_instruction': False, 'register_options': {'x': 0xCB }, },
                    {'m': 'SWAP r','datatype': '', 'opcode': opcodes.SWAP_r, 'length': 2, 'cycles': 8, 'jump_instruction':False, 'register_options': {'A': 0x37 } },
                    {'m': 'BIT b r','datatype': '', 'opcode': opcodes.BIT_7_r, 'length': 2, 'cycles': 8, 'jump_instruction': False, 'register_options': {'H': 0x7C }, 'oc_handler': NewOpcodeContext },
                    {'m': 'RES b r', 'datatype': '', 'opcode': opcodes.RES_n_r, 'length': 2, 'cycles': 8, 'jump_instruction': False, 'register_options' :{'A': 0x87} },
                    {'m': 'RL r'   , 'datatype': '', 'opcode': opcodes.RLC,  'length': 2, 'cycles': 8, 'jump_instruction': False, 'register_options': {'C': 0x11 } }
 ]

instructions = [{'m': 'XOR r'      , 'datatype': '',    'opcode': opcodes.XOR_r    , 'length': 1, 'cycles': 4,       'jump_instruction': False, 'register_options': {'A': 0xAF, 'C': 0xA9}    },
                {'m': 'LD r nn'    , 'datatype': '',    'opcode': opcodes.LD_r_nn  , 'length': 2, 'cycles': 8,       'jump_instruction': False, 'register_options': {'A': 0x3E, 'B': 0x06, 'C': 0x0E, 'L': 0x2E,'E': 0x1E, 'D': 0x16 } },
                {'m': 'LDH nn A'   , 'datatype': 'a8',  'opcode': opcodes.LDH_nn_A , 'length': 2, 'cycles': 12,      'jump_instruction': False, 'register_options': {'x': 0xE0 }   },
                {'m': 'JP nnnn'    , 'datatype': '',    'opcode': opcodes.JP_nnnn  , 'length': 3, 'cycles': [16, 16],'jump_instruction': True , 'register_options': {'x': 0xC3 }   },
                {'m': 'NOP'        , 'datatype': '',    'opcode': opcodes.NOP      , 'length': 1, 'cycles': 4,       'jump_instruction': False, 'register_options': {'x': 0x00 }   },
                {'m': 'DEC r'      , 'datatype': '',    'opcode': opcodes.DEC_r    , 'length': 1, 'cycles': 4,       'jump_instruction': False, 'register_options': {'B': 0x05, 'C': 0x0D, 'A': 0x3D, 'E': 0x1D, 'D': 0x15 } },
                {'m': 'DEC rr'     , 'datatype': '',    'opcode': opcodes.DEC_rr   , 'length': 1, 'cycles': 8,       'jump_instruction': False, 'register_options': {'BC': 0x0B } },
                {'m': 'DEC (rr)'   , 'datatype': '',    'opcode': opcodes.DEC_HL   , 'length': 1, 'cycles': 12,      'jump_instruction': False, 'register_options': {'(HL)': 0x35 } },
                {'m': 'LD rr nnnn' , 'datatype': '',    'opcode': opcodes.LDnn16d  , 'length': 3, 'cycles': 12,      'jump_instruction': False, 'register_options': {'HL': 0x21,'SP':0x31, 'BC': 0x01,'DE': 0x11  }, 'oc_handler': NewOpcodeContext },
                {'m': 'LD r nnnn'  , 'datatype': '',    'opcode': opcodes.LD_r_nnnn, 'length': 3, 'cycles': 16,      'jump_instruction': False, 'register_options': {'A': 0xFA } },
                {'m': 'LDHA nn'    , 'datatype': 'a8',  'opcode': opcodes.LDH_r_nn , 'length': 2, 'cycles': 12,      'jump_instruction': False, 'register_options': {'x': 0xF0   } },
                {'m': 'LDD (HL-) A', 'datatype': '',    'opcode': opcodes.LDD_HL_A , 'length': 1, 'cycles': 8,       'jump_instruction': False, 'register_options': {'x': 0x32   }, 'oc_handler': NewOpcodeContext  },
                {'m': 'LDI A (HL+)', 'datatype': '',    'opcode': opcodes.LDI_A_HL , 'length': 1, 'cycles': 8,       'jump_instruction': False, 'register_options': {'x': 0x2A   } },
                {'m': 'LDI (HL+) A', 'datatype': '',    'opcode': opcodes.LDI_HL_A , 'length': 1, 'cycles': 8,       'jump_instruction': False, 'register_options': {'x': 0x22   } },
                {'m': 'JRNZ nnnn'  , 'datatype': 'r8',  'opcode': opcodes.JRNZn    , 'length': 2, 'cycles': [8, 12], 'jump_instruction': True , 'register_options': {'x': 0x20   } },
                {'m': 'JRZ nn'     , 'datatype': 'r8',  'opcode': opcodes.JRZn     , 'length': 2, 'cycles': [8, 12], 'jump_instruction': True , 'register_options': {'x': 0x28   } },
                {'m': 'JPZ nnnn'   , 'datatype': 'a16', 'opcode': opcodes.JP_Z_nnnn, 'length': 3, 'cycles': [12, 16],'jump_instruction': True , 'register_options': {'x': 0xCA   } },
                {'m': 'JR nnnn'    , 'datatype': 'r8',  'opcode': opcodes.JRn      , 'length': 2, 'cycles': [12, 12],'jump_instruction': True , 'register_options': {'x': 0x18   } },
                {'m': 'DI'         , 'datatype': ''  ,  'opcode': opcodes.DI       , 'length': 1, 'cycles': 4,       'jump_instruction': False, 'register_options': {'x': 0xF3   } },
                {'m': 'CP nn'      , 'datatype': 'd8',  'opcode': opcodes.CP_n     , 'length': 2, 'cycles': 8,       'jump_instruction': False, 'register_options': {'x': 0xFE   }, 'oc_handler': NewOpcodeContext },
                {'m': 'EI'         , 'datatype': ''  ,  'opcode': opcodes.EI       , 'length': 1, 'cycles': 4,       'jump_instruction': False, 'register_options': {'x': 0xFB   } },
                {'m': 'LD (rr) nn' , 'datatype': 'd8',  'opcode': opcodes.LD_rr_nn , 'length': 2, 'cycles': 12,      'jump_instruction': False, 'register_options': {'(HL)': 0x36, '(DE)': 0x12 } },
                {'m': 'LD (r) r'   , 'datatype': ''  ,  'opcode': opcodes.LDCA     , 'length': 2, 'cycles': 8,       'jump_instruction': False, 'register_options': {'(C) A':  0xE2  }, 'oc_handler': NewOpcodeContext },
                {'m': 'LD r r'     , 'datatype': 'd8',  'opcode': opcodes.LD_n_n   , 'length': 1, 'cycles': 12,      'jump_instruction': False, 'register_options': {'A C': 0x79,'A B': 0x78,'C A': 0x4F, 'A E': 0x7B, 'H A': 0x67,'D A': 0x57,'A H': 0x7C, 'B A': 0x47, 'E A': 0x5F }},
                {'m': 'LD nnnn r'  , 'datatype': 'a16', 'opcode': opcodes.LD_nnnn_A, 'length': 3, 'cycles': 16,      'jump_instruction': False, 'register_options': {'A': 0xEA }, 'oc_handler': NewOpcodeContext },
                {'m': 'INC r'      , 'datatype': ''   , 'opcode': opcodes.INC_r    , 'length': 1, 'cycles': 4,       'jump_instruction': False, 'register_options': {'C': 0xC, 'B': 0x04, 'H': 0x24, 'E': 0x1C, 'L': 0x2C } },
                {'m': 'SUB r'      , 'datatype': ''   , 'opcode': opcodes.SUB_r    , 'length': 1, 'cycles': 4,       'jump_instruction': False, 'register_options': {'B': 0x90 } },
                {'m': 'CALL nnnn'  , 'datatype': 'a16', 'opcode': opcodes.CALL_nnnn, 'length': 3, 'cycles': 24,      'jump_instruction': False, 'register_options': {'x': 0xCD }, 'oc_handler': NewOpcodeContext },
                {'m': 'OR r'       , 'datatype': ''   , 'opcode': opcodes.OR_r     , 'length': 1, 'cycles': 4,       'jump_instruction': False, 'register_options': {'C': 0xB1,'B': 0xB0 } },
                {'m': 'LD (rr) r'  , 'datatype': ''   , 'opcode': opcodes.LDHL8A   , 'length': 1, 'cycles': 8,       'jump_instruction': False, 'register_options': {'(HL) A': 0x77}},
                {'m': 'RET'        , 'datatype': ''   , 'opcode': opcodes.RET      , 'length': 1, 'cycles': 16,      'jump_instruction': False, 'register_options': {'x': 0xC9 } },
                {'m': 'RETZ'       , 'datatype': ''   , 'opcode': opcodes.RET_Z    , 'length': 1, 'cycles': [8, 20], 'jump_instruction': True,  'register_options': {'x': 0xC8 } },
                {'m': 'RETNZ'      , 'datatype': ''   , 'opcode': opcodes.RET_NZ   , 'length': 1, 'cycles': [8, 20], 'jump_instruction': True,  'register_options': {'x': 0xC0 } },
                {'m': 'LD r (rr)'  , 'datatype': ''   , 'opcode': opcodes.LD_r_i16 , 'length': 1, 'cycles': 8,       'jump_instruction': False, 'register_options': {'A (DE)': 0x1A, 'E (HL)': 0x5E, 'D (HL)': 0x56, 'A (HL)': 0x7E}},
                {'m': 'PUSH rr'    , 'datatype': ''   , 'opcode': opcodes.PUSH_rr  , 'length': 1, 'cycles': 16,      'jump_instruction': False, 'register_options': {'BC': 0xC5, 'HL': 0xE5, 'DE': 0xD5, 'AF': 0xF5 } },
                {'m': 'RLA'        , 'datatype': ''   , 'opcode': opcodes.RLA      , 'length': 1, 'cycles': 4,       'jump_instruction': False, 'register_options': {'x': 0x17  } },
                {'m': 'POP rr'     , 'datatype': ''   , 'opcode': opcodes.POP_rr   , 'length': 1, 'cycles': 12,      'jump_instruction': False, 'register_options': {'BC': 0xC1,'HL': 0xE1,'DE': 0xD1,'AF': 0xF1} },
                {'m': 'INC rr'     , 'datatype': ''   , 'opcode': opcodes.INCnn    , 'length': 1, 'cycles': 8,       'jump_instruction': False, 'register_options': {'HL': 0x23, 'DE': 0x13} },
                {'m': 'CPL'        , 'datatype': ''   , 'opcode': opcodes.CPL      , 'length': 1, 'cycles': 4,       'jump_instruction': False, 'register_options': {'x': 0x2F} },
                {'m': 'AND nn'     , 'datatype': ''   , 'opcode': opcodes.AND_nn   , 'length': 2, 'cycles': 8,       'jump_instruction': False, 'register_options': {'x': 0xE6 } },
                {'m': 'AND r'      , 'datatype': ''   , 'opcode': opcodes.AND_r    , 'length': 1, 'cycles': 4,       'jump_instruction': False, 'register_options': {'C': 0xA1, 'A': 0xA7 } },
                {'m': 'RST nnH'    , 'datatype': ''   , 'opcode': opcodes.RST_nn   , 'length': 1, 'cycles': 16,      'jump_instruction': False, 'register_options': {'28H': 0xEF } },
                {'m': 'CLRFL'      , 'datatype': ''   , 'opcode': opcodes.CLRFL    , 'length': 1, 'cycles': 4,       'jump_instruction': False, 'register_options': {'x': 0xE3   } },
                {'m': 'SETFL'      , 'datatype': ''   , 'opcode': opcodes.SETFL    , 'length': 1, 'cycles': 4,       'jump_instruction': False, 'register_options': {'x': 0xE4   } },
                {'m': 'ADD rr rr'  , 'datatype': ''   , 'opcode': opcodes.ADD_rr_rr, 'length': 1, 'cycles': 8,       'jump_instruction': False, 'register_options': {'HL DE': 0x19}},
                {'m': 'ADD r r'    , 'datatype': ''   , 'opcode': opcodes.ADD_r_r  , 'length': 1, 'cycles': 4,       'jump_instruction': False, 'register_options': {'A A': 0x87  } },
                {'m': 'JP (rr)'    , 'datatype': ''   , 'opcode': opcodes.JP_HL    , 'length': 1, 'cycles': [4,4],       'jump_instruction': True,  'register_options': {'(HL)': 0xE9} }
               ]

def get_instruction_by_mnemonic(mnemonic):
    instructions = create_mnemonic_dictionary()

    for i in instructions:
        if i['m'] == mnemonic:
            return i

def create_cb_mnemonic_dictionary():
    result = {}
    for instruction in cb_instructions:
        result[instruction['m']] = instruction

    return result

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

def create_cb_opcode_metamap():
    result = [None] * 255
    for i in cb_instructions:
        for opcode in i['register_options'].values():
            result[opcode] = i
    return result

def create_opcode_metamap():
    result = [None] * 255
    for i in instructions:
        for opcode in i['register_options'].values():
            result[opcode] = i
    return result

def create_cb_opcode_map(element):
    result = [None] * 255
    for i in cb_instructions:
        for opcode in i['register_options'].values():
            result[opcode] = i[element]
    return result


def create_cb_opcode_contexts(cpu, mmu):
    result = [None] * 255
    opcode_meta = create_cb_opcode_metamap() 
    for i in cb_instructions:
        for opcode in i['register_options'].values():
            if i.get('oc_handler'):
                context = i['oc_handler'](cpu, mmu, i)
            else:
                context = OpcodeContext(cpu, mmu, i)
            
            result[opcode] = context
    return result

def create_opcode_contexts(cpu, mmu):
    result = [None] * 255
    opcode_meta = create_opcode_metamap() 
    for i in instructions:
        for opcode in i['register_options'].values():
            if i.get('oc_handler'):
                context = i['oc_handler'](cpu, mmu, i)
            else:
                context = OpcodeContext(cpu, mmu, i)

            result[opcode] = context
    return result

def create_opcode_map(element):
    result = [None] * 255
    for i in instructions:
        for opcode in i['register_options'].values():
            result[opcode] = i[element]
    return result
