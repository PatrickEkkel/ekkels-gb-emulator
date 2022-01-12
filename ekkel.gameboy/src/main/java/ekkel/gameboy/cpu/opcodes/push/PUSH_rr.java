package ekkel.gameboy.cpu.opcodes.push;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class PUSH_rr extends Opcode {

    public PUSH_rr() {
        super();
        this.length = 1;
        this.mnemonic.setMnemonic("PUSH");

    }

    private Registers register;
    protected void setRegister(Registers register) {
        this.register = register;

    }

    @Override
    public int[] toBinary() {
        return new int [] {this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.push(this.cpu.readRegister(this.register)).incPC();
        return  16;
    }
    @Override
    public String toString() {

        String result = String.format("%s %s",this.mnemonic.getMnemonic(), this.register.toString());
        return result;
    }
}
