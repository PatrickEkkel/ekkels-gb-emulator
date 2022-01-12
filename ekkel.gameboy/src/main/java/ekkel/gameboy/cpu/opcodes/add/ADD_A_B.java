package ekkel.gameboy.cpu.opcodes.add;

import core.cpu.registers.Registers;

public class ADD_A_B extends ADD_A_r {

    public ADD_A_B() {
        this.instr = 0x80;
        this.setLoadRegister(Registers.B);
    }
}
