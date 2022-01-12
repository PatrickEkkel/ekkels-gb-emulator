package ekkel.gameboy.cpu.opcodes.dec;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class DEC_r16 extends Opcode {


    private Registers rightRegister;

    @Override
    public int[] toBinary() {
        return new int[]{this.instr};
    }


    public void setRightRegister(Registers rightRegister) {
        this.rightRegister = rightRegister;
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.load(rightRegister).dec().store(rightRegister).incPC();
        return 8;
    }

    @Override
    public String toString() {
        return String.format("%s %s", this.mnemonic.getMnemonic(), this.rightRegister.toString());
    }
}
