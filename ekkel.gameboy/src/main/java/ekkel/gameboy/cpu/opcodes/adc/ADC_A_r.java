package ekkel.gameboy.cpu.opcodes.adc;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class ADC_A_r extends Opcode {
    protected Registers right;

    public ADC_A_r() {
        this.mnemonic.setMnemonic("ADC");
    }

    public void setRightRegister(Registers register) {
        this.right = register;
    }

    @Override
    public int[] toBinary() {
        return new int[]{this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        throw new NotImplementedException("ADC A r is not yet implemented");
    }

    @Override
    public String toString() {
        return String.format("%s A %s ", this.mnemonic.getMnemonic(), this.right.toString());
    }


}
