package ekkel.gameboy.cpu.opcodes.ldd;


import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;

public class LDD_HL_A extends Opcode {

    public LDD_HL_A() {
        this.instr = 0x32;
        this.mnemonic.setMnemonic("LDD");
    }

    @Override
    public int[] toBinary() {
        return new int[] {this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.load(Registers.A).load(Registers.HL).store().load(Registers.HL).dec().store(Registers.HL).incPC();
        return 8;
    }

    @Override
    public String toString() {
        return String.format("%s (%s) %s",this.mnemonic.getMnemonic(),"HL","A");
    }
}
