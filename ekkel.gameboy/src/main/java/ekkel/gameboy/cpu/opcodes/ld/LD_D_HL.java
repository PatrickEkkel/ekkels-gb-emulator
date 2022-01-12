package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_D_HL extends LD_r_i16 {

    public LD_D_HL() {
        this.instr = 0x56;
        this.setLeftLoadRegister(Registers.D);
        this.setRightLoadRegister(Registers.HL);
    }
}
