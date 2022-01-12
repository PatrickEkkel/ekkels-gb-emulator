package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_E_B extends LD_r_r {

    public LD_E_B() {
        this.instr = 0x58;
        this.setLeftRegister(Registers.E);
        this.setRightRegister(Registers.B);
    }
}
