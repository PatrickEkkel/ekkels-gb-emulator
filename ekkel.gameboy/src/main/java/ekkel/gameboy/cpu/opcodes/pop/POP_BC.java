package ekkel.gameboy.cpu.opcodes.pop;

import core.cpu.registers.Registers;

public class POP_BC extends POP_rr {

    public POP_BC() {
        this.instr = 0xC1;
        this.setRegister(Registers.BC);
    }
}
