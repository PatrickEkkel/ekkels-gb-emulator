package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_E_C extends LD_r_r {

    public LD_E_C() {
        this.instr = 0x59;
        this.setLeftRegister(Registers.E);
        this.setRightRegister(Registers.C);
    }
}
