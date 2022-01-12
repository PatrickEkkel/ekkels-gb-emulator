package ekkel.gameboy.cpu.opcodes.cb;

import core.cpu.registers.Registers;

public class RL_C extends RL_r {

    public RL_C() {
        this.instr = 0x11;
        this.setLoadRegister(Registers.C);
    }

}
