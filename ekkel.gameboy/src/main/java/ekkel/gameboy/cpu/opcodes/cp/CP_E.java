package ekkel.gameboy.cpu.opcodes.cp;

import core.cpu.registers.Registers;

public class CP_E  extends CP_r {

    public CP_E() {
        this.instr = 0xBB;
        this.setLoadRegister(Registers.E);
    }

}
