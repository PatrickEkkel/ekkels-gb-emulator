package ekkel.gameboy.cpu.opcodes.dec;

import core.cpu.registers.Registers;

public class DEC_SP extends DEC_r16 {

    public DEC_SP() {
        this.instr = 0x3B;
        this.setRightRegister(Registers.SP);
    }
}
