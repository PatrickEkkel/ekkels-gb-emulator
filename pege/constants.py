# Joypad Register
JP_REGISTER   = 0xFF00
# PPU LY register
LY_REGISTER   = 0xFF44
# LCD Control register
LCDC_REGISTER = 0xFF40
# Interrupt flag register
IF_REGISTER   = 0xFF0F
# Interrupt enable register
IE_REGISTER   = 0xFFFF 


# CPU Registers
r_A  = 10
r_B  = 20
r_C  = 30
r_D  = 40
r_E  = 50
r_H  = 51
r_L  = 52
r_F  = 60

r_AF = 70
r_BC = 80
r_DE = 90
r_HL = 95

# Stack Pointer
r_SP = 100
# Program counter
r_PC = 110

# CPU FLAGS 
Z = 120
N = 130
H = 140
C = 150

I = '-'
        


# Addressing modes
d8  = 151
d16 = 152
a8  = 153
a16 = 154
r8  = 155

# Bitwise operators
OR = 160
AND = 161
XOR = 162
# CPL is short for complement register, which is a bitwise NOT
CPL = 163
NOT = 164
SHIFT_RIGHT = 165
SHIFT_LEFT = 166

