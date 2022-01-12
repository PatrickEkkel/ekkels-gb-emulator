package ekkel.gameboy.cpu.opcodes.dec;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Register;
import core.cpu.registers.Registers;

public class DEC_r extends Opcode {
    private Registers register;
    protected void setLoadRegister(Registers register) {
        this.register = register;
        this.mnemonic.setMnemonic("DEC");
    }
    @Override
    public int[] toBinary() {
        return new int [] {this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.load(register).dec().flags(Flags.Z,1,Flags.H,Flags.E).store(register).incPC();
        return 4;
    }

    @Override
    public String toString() {
        return String.format("%s %s",this.mnemonic.getMnemonic(), this.register.toString());
    }
}
