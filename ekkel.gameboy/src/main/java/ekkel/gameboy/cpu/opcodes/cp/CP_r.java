package ekkel.gameboy.cpu.opcodes.cp;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class CP_r extends Opcode {

    private Registers register;

    protected void setLoadRegister(Registers register) {
        this.register = register;
        this.mnemonic.setMnemonic("CP");
    }

    @Override
    public int[] toBinary() {
        return new int[]{this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        throw new NotImplementedException("CP r is not yet implemented");
    }

    @Override
    public String toString() {
        return String.format("%s %s", this.mnemonic.getMnemonic(), register);
    }
}
