package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_D_A  extends LD_r_r {

    public LD_D_A() {
        this.setLeftRegister(Registers.D);
        this.setRightRegister(Registers.A);
        this.instr = 0x57;
    }

}
