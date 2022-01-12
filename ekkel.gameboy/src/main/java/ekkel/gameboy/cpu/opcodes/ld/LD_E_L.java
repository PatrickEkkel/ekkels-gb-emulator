package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_E_L extends LD_r_r {

    public LD_E_L() {
        this.instr = 0x5D;
        this.setLeftRegister(Registers.E);
        this.setRightRegister(Registers.L);
    }

}
