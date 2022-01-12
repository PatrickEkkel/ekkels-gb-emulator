package ekkel.gameboy.cpu.opcodes.adc;

import core.cpu.Flags;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.mmu.MemoryAddress;

public class ADC_A_d8 extends Opcode {

    public ADC_A_d8() {
        this.instr = 0xCE;
        this.mnemonic.setMnemonic("ADC A");
    }

    @Override
    public int[] toBinary() {
        // It should be a memory address
        MemoryAddress data = (MemoryAddress) this.getData();
        return new int[] {this.instr,data.getLowByte()};
    }

    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        this.loadD8Computables();
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        dsl.loadD8().load(Registers.A).add().adc().flags(Flags.Z,0,Flags.H,Flags.C).store(Registers.A).incPC();
        return 8;
    }
    @Override
    public String toString() {
        String data = "nn";
        if(this.getData() != null) {
            data = this.getData().toString();
        }
        return String.format("%s %s", this.mnemonic.getMnemonic(),data);
    }

}
