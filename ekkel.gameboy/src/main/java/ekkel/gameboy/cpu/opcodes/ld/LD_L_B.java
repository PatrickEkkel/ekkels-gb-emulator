package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_L_B  extends LD_r_r {

    public LD_L_B() {
        this.instr = 0x68;
        this.setLeftRegister(Registers.L);
        this.setRightRegister(Registers.B);
    }

}
