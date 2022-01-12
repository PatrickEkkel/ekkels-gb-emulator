package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_E_H extends LD_r_r {

    public LD_E_H() {
        this.instr = 0x5C;
        this.setLeftRegister(Registers.E);
        this.setRightRegister(Registers.H);
    }
}
