package ekkel.gameboy.cpu.opcodes.branch;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.mmu.MemoryAddress;

public class JR_r8 extends Opcode {

    public JR_r8() {
        this.length = 2;
        this.instr = 0x18;
        this.mnemonic.setMnemonic("JR");
    }

    @Override
    public int[] toBinary() {
        MemoryAddress mem = (MemoryAddress) this.getComputables().get(0);
        return new int[] {this.instr, mem.getLowByte()};
    }

    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        loadS8Computables();
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException{
        dsl.loadS8().load(Registers.PC).add().store(Registers.PC).incPC();
        return 12;
    }

    @Override
    public String toString() {
        String address = "s8";
        if (this.getData() != null) {
            address = this.getData().toString();
        }
        String result = String.format("%s %s", this.mnemonic.getMnemonic(), address);
        return result;
    }
}
