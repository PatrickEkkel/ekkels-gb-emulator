package ekkel.gameboy.cpu.opcodes.dec;

import core.cpu.registers.Registers;

public class DEC_DE extends DEC_r16 {

    public DEC_DE() {
        this.instr = 0x1B;
        this.setRightRegister(Registers.DE);
    }

}
