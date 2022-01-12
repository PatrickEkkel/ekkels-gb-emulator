package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_HL_A extends LD_i16_r  {

    public LD_HL_A() {
        this.instr = 0x77;
        this.setLeftLoadRegister(Registers.HL);
        this.setRightLoadRegister(Registers.A);
    }
}
