package ekkel.gameboy.cpu.opcodes.cb;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class BIT_r extends Opcode {

    Integer position;
    Registers register;


    protected void setPosition(int position) {
        this.position = position;
    }

    protected void setLoadRegister(Registers register) {
        this.register = register;
    }

    public BIT_r() {
        this.mnemonic.setMnemonic("BIT");
    }

    @Override
    public int[] toBinary() {
        return new int[] {this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        throw new NotImplementedException("BIT r is not yet implemented");
    }

    @Override
    public String toString() {
        return String.format("%s %s %s",this.mnemonic.getMnemonic(),this.position.toString(),register);
    }
}
