package ekkel.gameboy.cpu.opcodes.cb;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class SWAP_r extends Opcode {

    private Registers register;

    public SWAP_r() {
        this.mnemonic.setMnemonic("SWAP");
    }

    protected void setLoadRegister(Registers register) {
        this.register = register;
    }

    @Override
    public int[] toBinary() {
        return new int[]{this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.load(register).bitwiseSwap().flags(Flags.Z,0,0,0).store(Registers.A).incPC().incPC();
        return 8;
    }

    @Override
    public String toString() {
        return String.format("%s %s",this.mnemonic.getMnemonic(),this.register.toString());
    }
}
