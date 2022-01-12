package ekkel.gameboy.cpu.opcodes.or;

import core.cpu.registers.Registers;

public class OR_C extends OR_r {

    public OR_C() {
        this.instr = 0xB1;
        this.setRegister(Registers.C);
    }

}
