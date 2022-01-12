package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class LD_r_r  extends Opcode {

    private Registers left;
    private Registers right;

    public LD_r_r() {
        this.length = 1;
        this.mnemonic.setMnemonic("LD");
    }

    protected void setLeftRegister(Registers register) {
        this.left = register;
    }
    protected void setRightRegister(Registers register) {
        this.right = register;
    }

    @Override
    public int[] toBinary() {
        return new int[] { this.instr };
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.load(this.right).store(this.left).incPC();
        return 4;
    }


    @Override
    public String toString() {
        return String.format("%s %s %s",this.mnemonic.getMnemonic(),this.left,this.right);
    }
}
