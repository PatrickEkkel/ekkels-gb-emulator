package ekkel.gameboy.cpu.opcodes.and;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class AND_r extends Opcode {

    public AND_r() {
        this.mnemonic.setMnemonic("AND");
    }

    protected Registers register;
    public void setLoadRegister(Registers register) {
        this.register = register;
        this.mnemonic.setRegister(register.toString());
    }

    @Override
    public int[] toBinary() {
        return new int[] { this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        throw new NotImplementedException("AND r is not yet implemented");
    }

    @Override
    public String toString() {
       return String.format("%s %s",this.mnemonic.getMnemonic(), register.toString());
    }
}
