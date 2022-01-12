package ekkel.gameboy.cpu.opcodes.cb;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class RR_r extends Opcode {

    private Registers register;

    protected void setLoadRegister(Registers register) {
        this.register = register;
    }

    public RR_r() {
        this.instr = 0x19;
        this.mnemonic.setMnemonic("RR");
    }

    @Override
    public int[] toBinary() {
        return new int[] {this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.load(register).carryLsb().shiftRight(1).rotate(Flags.C,7).flags(Flags.Z,0,0,Flags.C).store(register).incPC().incPC();
        return 8;
    }

    @Override
    public String toString() {
        return String.format("%s %s",this.mnemonic.getMnemonic(),this.register.toString());
    }
}
