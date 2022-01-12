package ekkel.gameboy.cpu.opcodes.add;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class ADD_rr_rr extends Opcode {

    private Registers leftRegister;
    private Registers rightRegister;


    public ADD_rr_rr() {
        this.mnemonic.setMnemonic("ADD");
    }


    public void setLeftRegister(Registers leftRegister) {
        this.leftRegister = leftRegister;
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
        dsl.load(leftRegister).load(rightRegister).add().flags(Flags.E,0,Flags.H,Flags.C).store(leftRegister).incPC();
        return 8;
    }

    @Override
    public String toString() {
        return String.format("%s %s %s",this.mnemonic.getMnemonic(), this.leftRegister.toString(),this.rightRegister.toString());
    }
}
