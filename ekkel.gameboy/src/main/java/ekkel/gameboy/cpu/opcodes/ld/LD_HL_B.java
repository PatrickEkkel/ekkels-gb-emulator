package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_HL_B extends LD_i16_r {

    public LD_HL_B() {
        this.instr = 0x70;
        this.setLeftLoadRegister(Registers.HL);
        this.setRightLoadRegister(Registers.B);
    }

}
