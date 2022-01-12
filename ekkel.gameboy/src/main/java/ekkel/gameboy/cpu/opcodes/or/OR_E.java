package ekkel.gameboy.cpu.opcodes.or;

import core.cpu.registers.Registers;

public class OR_E extends OR_r {

    public OR_E() {
        this.instr = 0xB3;
        this.setRegister(Registers.E);
    }

}
