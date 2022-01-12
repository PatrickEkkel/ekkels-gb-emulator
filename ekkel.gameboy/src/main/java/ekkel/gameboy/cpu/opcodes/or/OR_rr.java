package ekkel.gameboy.cpu.opcodes.or;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class OR_rr extends Opcode {

    private Registers leftRegister;
    private Registers rightRegister;

    protected void setLeftRegister(Registers leftRegister) {
        this.leftRegister = leftRegister;
    }
    protected void setRightRegister(Registers rightRegister) {
        this.rightRegister = rightRegister;
    }

    @Override
    public int[] toBinary() {
        return new int[] { this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        this.dsl.load(leftRegister).loadIR16(rightRegister).bitwiseOr().flags(Flags.Z,0,0,0).incPC();
        return 8;
    }

    @Override
    public String toString() {
        return String.format("%s (%s)",this.mnemonic.getMnemonic(),this.rightRegister.toString());
    }
}
