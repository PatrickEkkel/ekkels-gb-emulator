package ekkel.gameboy.cpu.opcodes.ldi;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class LDI_HL_A extends Opcode {

    public LDI_HL_A() {
        this.instr = 0x22;
        this.mnemonic.setMnemonic("LDI");
    }

    @Override
    public int[] toBinary() {
        return new int[] {this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.load(Registers.A).load(Registers.HL).store().load(Registers.HL).inc().store(Registers.HL).incPC();
        return 8;
    }

    @Override
    public String toString() {
        return String.format("%s %s %s",this.mnemonic.getMnemonic(),"HL","A");
    }
}
