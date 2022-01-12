package ekkel.gameboy.cpu.opcodes.or;

import core.cpu.registers.Registers;

public class OR_A extends OR_r {

    public OR_A() {
        this.instr = 0xB7;
        this.setRegister(Registers.A);
    }
}
