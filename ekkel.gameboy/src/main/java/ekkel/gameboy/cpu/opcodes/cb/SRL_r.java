package ekkel.gameboy.cpu.opcodes.cb;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class SRL_r extends Opcode {

    private Registers register;


    public void setLoadRegister(Registers register) {
        this.register = register;
    }

    public SRL_r() {
        this.mnemonic.setMnemonic("SRL");
    }

    @Override
    public int[] toBinary() {
        return new int[] { this.instr };
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.load(register).carryLsb().shiftRight(1).flags(Flags.Z,0,0,Flags.C).store(register).incPC().incPC();
        return 8;
    }

    @Override
    public String toString() {
        return String.format("%s %s",this.mnemonic.getMnemonic(),this.register );
    }
}
