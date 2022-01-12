package ekkel.gameboy.cpu.opcodes.ld;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
// Blargg test faalt nog op deze
public class LD_HL_d8  extends Opcode {

    public LD_HL_d8() {
        this.instr = 0x36;
        this.mnemonic.setMnemonic("LD (HL)");
    }


    @Override
    public int[] toBinary() {
        return new int[] {this.instr,this.getData().getLowByte()};
    }

    @Override
    public void dryRun() throws NotImplementedException, IllegalAccessException {
        loadD8Computables();
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
            dsl.loadD8().load(Registers.HL).store().incPC();
        return 12;
    }


    @Override
    public String toString() {
        String data = "nn";
        if(this.getData() != null) {
            data = this.getData().toString();
        }
        return String.format("%s %s",this.mnemonic.getMnemonic(), data);
    }
}
