package ekkel.gameboy.cpu.opcodes.inc;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class INC_r  extends Opcode {

    private Registers registers;

    public INC_r() {
        this.mnemonic.setMnemonic("INC");
    }

    @Override
    public int[] toBinary() {
        return new int[] {this.instr};
    }

    protected void setLoadRegister(Registers register) {
        this.registers = register;
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        // Z 0 H -
        dsl.load(registers).inc().flags(Flags.Z,0,Flags.H,Flags.E).store(registers).incPC();
        return 4;
    }

    @Override
    public String toString() {
        return String.format("%s %s", this.mnemonic.getMnemonic(), this.registers.toString());
    }
}
