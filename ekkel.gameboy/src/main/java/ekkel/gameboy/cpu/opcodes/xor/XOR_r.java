package ekkel.gameboy.cpu.opcodes.xor;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
public class XOR_r  extends Opcode {

    protected Registers register;

    public XOR_r() {
        this.mnemonic.setMnemonic("XOR");
    }

    public void setLoadRegister(Registers register) {
        this.register = register;
    }

    @Override
    public int[] toBinary() {
        return new int[] { this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.load(register).load(Registers.A).xor().flags(Flags.Z,0,0,0).store(Registers.A).incPC();
        return 4;
    }

    @Override
    public String toString() {
        return String.format("%s %s",this.mnemonic.getMnemonic(), this.register.toString());
    }
}
