package ekkel.gameboy.cpu.opcodes.pop;

import core.cpu.registers.Registers;

public class POP_DE extends POP_rr {

    public POP_DE() {
        this.instr = 0xD1;
        this.setRegister(Registers.DE);
    }
}
