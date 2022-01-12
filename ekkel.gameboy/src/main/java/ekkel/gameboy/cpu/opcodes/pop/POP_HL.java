package ekkel.gameboy.cpu.opcodes.pop;

import core.cpu.registers.Registers;

public class POP_HL extends POP_rr {

    public POP_HL() {
        this.setRegister(Registers.HL);
        this.instr = 0xE1;
    }
}
