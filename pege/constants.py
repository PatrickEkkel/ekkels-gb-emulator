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
A = 10
B = 20
C = 30
D = 40
E = 50
F = 60

AF = 70
BC = 80
DE = 90

# Stack Pointer
SP = 100
# Program counter
PC = 110

# CPU FLAGS 
Z = 120
N = 130
H = 140
C = 150


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

