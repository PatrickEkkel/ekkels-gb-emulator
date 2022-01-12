package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_E_E extends LD_r_r {

    public LD_E_E() {
        this.instr = 0x5B;
        this.setLeftRegister(Registers.E);
        this.setRightRegister(Registers.E);
    }
}
