package ekkel.gameboy.cpu.opcodes.sub;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class SUB_r extends Opcode {

    private Registers registers;
    protected void setLoadRegister(Registers register) {
        this.registers = register;
    }
    public SUB_r() {
        this.mnemonic.setMnemonic("SUB");
    }

    @Override
    public int[] toBinary() {
        return new int[] {this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        throw new NotImplementedException("SUB r is not yet implemented");
    }


    @Override
    public String toString() {
        return String.format("%s %s", this.mnemonic.getMnemonic(), this.registers.toString());
    }
}
