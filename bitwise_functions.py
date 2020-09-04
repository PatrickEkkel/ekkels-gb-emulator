# https://gist.github.com/cincodenada/6557582
# do a left bitwise rotation, 
def rotate_left(num, bits):
            bit = num & (1 << (bits-1))
            num <<= 1
            if(bit):
                num |= 1
            num &= (2**bits-1)

            return num

# https://gist.github.com/cincodenada/6557582
# do a right bitwise rotation,
def rotate_right(num, bits):
    num &= (2**bits-1)
    bit = num & 1
    num >>= 1
    if(bit):
        num |= (1 << (bits-1))

    return num


# do a bitwise shift left, this function will keep the boundaries of 8-bits 
# and will not cause to increase the size of the byte
def shift_left(num, bits):
    num &= (2**bits-1)
    num <<= 1
    num &= (2**bits-1)
    return num


# take two 8 bit values and concatinate them into one 16 bit value
def merge_8bit_values(a,b):
    return (a << 8) | b
