package ekkel.gameboy.cpu.opcodes.ldh;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.mmu.MemoryAddress;
import ekkel.gameboy.cpu.opcodes.ld.LD_xx;

public class LDH_xx  extends LD_xx {

    public LDH_xx() {
        this.length = 2;
        this.setLoadRegister(Registers.A);
        this.mnemonic.setMnemonic("LDH");
    }

    @Override
    public int[] toBinary() {
        MemoryAddress data = (MemoryAddress) this.getData();
        return new int[] {this.instr, data.getValue()};
    }

    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        this.loadD8Computables();
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        return 0;
    }

    @Override
    public String toString() {
        String address = "nn";
        if(this.getData() != null) {
            address = this.getData().toString();
        }



        return String.format("%s (FF00+%s)",this.mnemonic.getMnemonic(),address);
    }
}
