package ekkel.gameboy.cpu.opcodes.or;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class OR_r extends Opcode {

    private Registers register;

    protected void setRegister(Registers register) {
        this.register = register;
    }
    public OR_r() {
        this.mnemonic.setMnemonic("OR");
    }

    @Override
    public int[] toBinary() {
        return new int [] { this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.load(Registers.A).load(register).bitwiseOr().flags(Flags.Z,0,0,0).store(Registers.A).incPC();
        return 4;
    }

    @Override
    public String toString() {
        return String.format("%s %s",this.mnemonic.getMnemonic(),register.toString());
    }
}
