package ekkel.gameboy.cpu.opcodes.or;

import core.cpu.registers.Registers;

public class OR_L extends OR_r {

    public OR_L() {
        this.instr = 0xB5;
        this.setRegister(Registers.L);
    }
}
