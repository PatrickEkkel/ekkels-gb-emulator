package ekkel.gameboy.cpu.opcodes.misc;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;

public class STOP extends Opcode {

    public STOP() {
        this.instr = 0x10;
        this.mnemonic.setMnemonic("STOP");
    }

    @Override
    public int[] toBinary() {
        return new int[] { this.instr};
    }

    @Override
    public int execute() throws NotImplementedException, IllegalAccessException {
        // STOP doing anything..
        // don't stop, because we are lacking interrupts at the moment
        // otherwise the CPU will hang forever here.
        //dsl.stop();

        // implemented as NOP
        dsl.incPC();
        return 4;
    }
}
