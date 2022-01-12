package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_E_d8 extends LD_r_d8 {

    public LD_E_d8() {
        this.instr = 0x1E;
        this.setLoadRegister(Registers.E);
    }

}
