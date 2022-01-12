package ekkel.gameboy.cpu.opcodes.cp;

import core.cpu.registers.Registers;

public class CP_B extends CP_r {

    public CP_B() {
        this.instr = 0xB8;
        this.setLoadRegister(Registers.B);
    }

}
