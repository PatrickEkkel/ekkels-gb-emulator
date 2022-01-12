package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.registers.Registers;

public class LD_A_DE  extends LD_r_i16 {


    public LD_A_DE() {
        this.instr = 0x1A;
        this.setLeftLoadRegister(Registers.A);
        this.setRightLoadRegister(Registers.DE);
    }

    @Override
    public String toString() {
        return String.format(" %s %s (%s)",this.mnemonic.getMnemonic(),this.leftRegister, this.rightRegister.toString());
    }
}
