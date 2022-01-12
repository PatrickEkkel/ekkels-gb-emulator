package ekkel.gameboy.cpu.opcodes.pop;

import core.cpu.registers.Registers;

public class POP_AF extends POP_rr {

    public POP_AF() {
        this.instr = 0xF1;
        this.setRegister(Registers.AF);
    }
}
