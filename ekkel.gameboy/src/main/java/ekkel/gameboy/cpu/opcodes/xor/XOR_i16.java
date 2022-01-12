package ekkel.gameboy.cpu.opcodes.xor;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class XOR_i16 extends Opcode {

    private Registers register;

    public void setLoadRegister(Registers register) {
        this.register = register;
    }

    public XOR_i16() {
        this.mnemonic.setMnemonic("XOR");
    }

    @Override
    public int[] toBinary() {
        return new int[] {this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.loadIR16(register).load(Registers.A).xor().flags(Flags.Z,0,0,0).store(Registers.A).incPC();
        return 8;
    }

    @Override
    public String toString() {
        return String.format("%s (%s)",this.mnemonic.getMnemonic(),register.toString());
    }
}
