package ekkel.gameboy.cpu.opcodes.pop;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class POP_rr extends Opcode {

    public POP_rr () {
        this.length = 1;
        this.mnemonic.setMnemonic("POP");
    }
    private Registers register;
    protected void setRegister(Registers register) {
        this.register = register;
    }

    @Override
    public int[] toBinary() {
        return new int[] { this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        this.dsl.pop().store(register).incPC();
        return 12;
    }
    public String toString() {

        String result = String.format("%s %s",this.mnemonic.getMnemonic(), this.register.toString());
        return result;
    }
}
