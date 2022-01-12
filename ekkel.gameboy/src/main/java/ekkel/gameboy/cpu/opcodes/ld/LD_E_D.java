package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_E_D extends LD_r_r {

    public LD_E_D() {
        this.instr = 0x5A;
        this.setLeftRegister(Registers.E);
        this.setRightRegister(Registers.D);
    }
}
