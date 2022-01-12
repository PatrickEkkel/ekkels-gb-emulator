package ekkel.gameboy.cpu.opcodes.inc;

import core.cpu.registers.Registers;

import javax.swing.*;

public class INC_L extends INC_r {

    public INC_L() {
        this.instr = 0x2c;
        this.setLoadRegister(Registers.L);
    }

}
