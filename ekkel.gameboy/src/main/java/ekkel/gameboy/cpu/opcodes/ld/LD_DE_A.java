package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_DE_A extends LD_i16_r {

    public LD_DE_A() {
        this.instr = 0x12;
        this.setLeftLoadRegister(Registers.DE);
        this.setRightLoadRegister(Registers.A);
    }

}
