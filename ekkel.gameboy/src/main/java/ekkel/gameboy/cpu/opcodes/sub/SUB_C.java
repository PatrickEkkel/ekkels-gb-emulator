package ekkel.gameboy.cpu.opcodes.sub;

import core.cpu.registers.Registers;

public class SUB_C extends SUB_r {

    public SUB_C() {
        this.instr = 0x91;
        this.setLoadRegister(Registers.C);
    }
}
