package ekkel.gameboy.cpu.opcodes.inc;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class INC_nn extends Opcode {

    private Registers register;
    protected int cycles;
    public INC_nn() {
        this.mnemonic.setMnemonic("INC");
        this.length = 1;
    }
    protected void setRegister(Registers register) {
        this.register = register;
    }

    @Override
    public int[] toBinary() {
        return new int[] { this.instr };
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.load(this.register).inc().store(this.register).incPC();
        return cycles;
    }

    @Override
    public String toString() {
        String result = String.format("%s %s",this.mnemonic.getMnemonic(), this.register.toString());
        return result;
    }
}
