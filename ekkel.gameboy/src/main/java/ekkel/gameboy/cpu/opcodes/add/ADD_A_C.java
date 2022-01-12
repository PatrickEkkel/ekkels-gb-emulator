package ekkel.gameboy.cpu.opcodes.add;

import core.cpu.registers.Registers;

public class ADD_A_C extends ADD_A_r {

    public ADD_A_C() {
        this.instr = 0x81;
        this.setLoadRegister(Registers.C);
    }
}
