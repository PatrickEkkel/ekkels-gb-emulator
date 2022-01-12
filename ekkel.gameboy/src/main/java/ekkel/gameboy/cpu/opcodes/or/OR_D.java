package ekkel.gameboy.cpu.opcodes.or;

import core.cpu.registers.Registers;

public class OR_D  extends OR_r {

    public OR_D() {
        this.instr = 0xB2;
        this.setRegister(Registers.D);
    }



}
