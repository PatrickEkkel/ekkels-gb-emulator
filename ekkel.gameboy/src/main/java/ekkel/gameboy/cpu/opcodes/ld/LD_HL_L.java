package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_HL_L extends LD_i16_r {

    public LD_HL_L() {
        this.instr = 0x75;
        this.setLeftLoadRegister(Registers.HL);
        this.setRightLoadRegister(Registers.L);
    }
}
