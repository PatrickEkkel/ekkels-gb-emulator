package ekkel.gameboy.cpu.opcodes.or;

import core.cpu.registers.Registers;

public class OR_B  extends OR_r {

    public OR_B() {
        this.instr = 0xB0;
        this.setRegister(Registers.B);
    }
}
