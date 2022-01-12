package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.MemoryAddress;

public class LD_i8_r extends LD_xx {

    @Override
    public int[] toBinary() {
        MemoryAddress data = (MemoryAddress) this.getData();
        return new int[] {this.instr,data.getLowByte(),data.getHighByte()};
    }

    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        this.loadD8Computables();
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        throw new NotImplementedException("LD i8 r is not yet implemented");
    }

    @Override
    public String toString() {
        return String.format("%s (%s) %s",this.mnemonic.getMnemonic(),this.getData(),register);
    }
}
