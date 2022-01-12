package ekkel.gameboy.cpu.opcodes.cp;

import core.cpu.registers.Registers;

public class CP_C extends CP_r {

    public CP_C() {
        this.instr = 0xB9;
        this.setLoadRegister(Registers.C);
    }

}
