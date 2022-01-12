package ekkel.gameboy.cpu.opcodes.branch;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.mmu.MemoryAddress;

/**
 * Unconditional Jump to immediate 16 bit address
 */
public class JP_a16 extends Opcode {

    private MemoryAddress address;

    public JP_a16() {
        this.length = 3;
        this.instr = 0xc3;

        this.mnemonic.setMnemonic("JP");
    }

    @Override
    public int[] toBinary() {
        MemoryAddress mem = (MemoryAddress) this.getComputables().get(0);
        return new int[]{this.instr, mem.getLowByte(), mem.getHighByte()};
    }

    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        this.loadD16Computables();
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        this.dsl.loadA16().store(Registers.PC);
        return 16;
    }

    @Override
    public String toString() {
        String address = "nnnn";
        if (this.address != null) {
            address = this.address.toString();
        }
        String result = String.format("%s %s", this.mnemonic.getMnemonic(), address);
        return result;
    }
}
