package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class LD_xx extends Opcode {

    public LD_xx() {
        this.mnemonic.setMnemonic("LD");
    }
    @Override
    public int[] toBinary() {
        return new int[0];
    }
    protected Registers register;
    public void setLoadRegister(Registers register) {
        this.register = register;
        this.mnemonic.setRegister(register.toString());
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        return 0;
    }
}
