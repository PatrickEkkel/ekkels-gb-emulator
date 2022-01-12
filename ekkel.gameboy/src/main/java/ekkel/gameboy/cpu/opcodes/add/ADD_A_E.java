package ekkel.gameboy.cpu.opcodes.add;

import core.cpu.registers.Registers;

public class ADD_A_E extends ADD_A_r {

    public ADD_A_E() {
        this.instr = 0x83;
        setLoadRegister(Registers.E);
    }
}
