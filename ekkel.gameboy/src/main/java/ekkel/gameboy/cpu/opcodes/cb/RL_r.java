package ekkel.gameboy.cpu.opcodes.cb;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class RL_r extends Opcode  {

    protected Registers register;
    public void setLoadRegister(Registers register) {
        this.register = register;
        this.mnemonic.setRegister(register.toString());
    }


    public RL_r() {
        this.mnemonic.setMnemonic("RL");
    }

    @Override
    public int[] toBinary() {
        return new int[] { this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        throw new NotImplementedException("RL r is not yet implemented");
    }

    @Override
    public String toString() {
        return String.format(this.mnemonic.getMnemonic(),this.register.toString());
    }
}
