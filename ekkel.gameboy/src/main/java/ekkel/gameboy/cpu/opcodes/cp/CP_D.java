package ekkel.gameboy.cpu.opcodes.cp;

import core.cpu.registers.Registers;

public class CP_D extends CP_r {

    public CP_D() {
        this.instr = 0xBA;
        this.setLoadRegister(Registers.D);
    }

}
