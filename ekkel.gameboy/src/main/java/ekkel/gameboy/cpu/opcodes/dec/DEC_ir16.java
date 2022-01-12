package ekkel.gameboy.cpu.opcodes.dec;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class DEC_ir16 extends Opcode {


    private Registers rightRegister;

    public DEC_ir16() {
        this.mnemonic.setMnemonic("DEC");
    }

    public void setRightRegister(Registers rightRegister) {
        this.rightRegister = rightRegister;
    }


    @Override
    public int[] toBinary() {
        return new int[] {this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.loadIR16(this.rightRegister).dec().load(rightRegister).store().incPC();
        return 12;
    }

    @Override
    public String toString() {
        return String.format("%s (%s)",this.mnemonic.getMnemonic(),this.rightRegister.toString());
    }
}
