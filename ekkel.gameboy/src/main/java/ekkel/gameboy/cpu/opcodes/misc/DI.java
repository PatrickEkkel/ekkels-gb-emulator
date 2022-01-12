package ekkel.gameboy.cpu.opcodes.misc;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.mmu.MemoryAddress;
import core.mmu.MemoryValue;
import ekkel.gameboy.cpu.IOMap;

/**
 * Set InterruptFlag to 0x0000 (Disable Interrupts)
 */
public class DI extends Opcode {

    public DI() {
        this.length = 1;
        this.instr = 0xf3;
        this.mnemonic.setMnemonic("DI");
    }

    @Override
    public int[] toBinary() {
        return new int [] {this.instr};
    }

    @Override
    public int execute() throws NotImplementedException {
        dsl.load(MemoryAddress.fromValue(IOMap.IE)).store(MemoryValue.fromValue(0x0000)).incPC();
        return 4;
    }


    @Override
    public String toString() {
        String result = String.format("%s",this.mnemonic.getMnemonic());
        return result;
    }
}
