package ekkel.gameboy.cpu.opcodes.or;

import core.cpu.registers.Registers;

public class OR_H extends OR_r {

    public OR_H() {
        this.instr = 0xB4;
        this.setRegister(Registers.H);
    }
}
