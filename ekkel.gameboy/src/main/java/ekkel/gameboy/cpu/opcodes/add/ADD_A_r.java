package ekkel.gameboy.cpu.opcodes.add;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class ADD_A_r extends Opcode {

    private Registers register;

    public ADD_A_r() {
        this.mnemonic.setMnemonic("ADD A");
    }

    public void setLoadRegister(Registers register) {
        this.register = register;
    }

    @Override
    public int[] toBinary() {
        return new int[]{this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.load(register).load(Registers.A).add().flags(Flags.Z,0,Flags.H,Flags.C).store(Registers.A).incPC();
        return 4;
    }

    @Override
    public String toString() {
        return String.format("%s %s ",this.mnemonic.getMnemonic(), this.register.toString());
    }
}
