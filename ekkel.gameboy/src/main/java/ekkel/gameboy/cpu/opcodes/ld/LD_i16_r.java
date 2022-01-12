package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class LD_i16_r extends Opcode {

    protected Registers rightRegister;
    protected Registers leftRegister;

    public void setLeftLoadRegister(Registers register) {
        this.leftRegister = register;
    }

    public void setRightLoadRegister(Registers register) {
        this.rightRegister = register;
    }

    public LD_i16_r() {
        this.mnemonic.setMnemonic("LD");
    }

    @Override
    public int[] toBinary() {
        return new int[] {this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {

        this.dsl.load(this.rightRegister).load(leftRegister).store().incPC();

        return 8;
    }

    @Override
    public String toString() {
        return String.format("%s (%s) %s",this.mnemonic.getMnemonic(),leftRegister.toString(),rightRegister.toString());
    }
}
