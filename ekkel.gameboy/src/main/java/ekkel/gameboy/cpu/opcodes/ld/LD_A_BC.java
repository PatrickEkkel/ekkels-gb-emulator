package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_A_BC extends LD_r_i16 {

    public LD_A_BC() {
        this.instr = 0x0A;
        this.setLeftLoadRegister(Registers.A);
        this.setRightLoadRegister(Registers.BC);
    }

}
