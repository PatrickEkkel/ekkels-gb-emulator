package ekkel.gameboy.cpu.opcodes.ldi;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class LDI_A_HL extends Opcode {

    public LDI_A_HL() {
        this.mnemonic.setMnemonic("LDI");
        this.length = 1;
        this.instr = 0x2A;
    }


    @Override
    public int[] toBinary() {
        return new int[] {this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
       dsl.loadIR16(Registers.HL).store(Registers.A).load(Registers.HL).inc().store(Registers.HL).incPC();
        return 8;
    }

    @Override
    public String toString() {
        return String.format("%s A HL",this.mnemonic.getMnemonic(),"A","HL");
    }
}
