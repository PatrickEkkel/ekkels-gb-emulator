package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_D_D  extends LD_r_r {

    public LD_D_D() {
        this.setLeftRegister(Registers.D);
        this.setRightRegister(Registers.D);
        this.instr = 0x52;
    }

}
