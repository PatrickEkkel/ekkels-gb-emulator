package roms;

import core.rom.RomLoader;
import java.io.IOException;

public class OP_R_IMM_04 extends BlarggTestRom {

    public OP_R_IMM_04() throws IOException {
        String filename = "04-op r,imm.gb";
        this.load(filename);
    }

}
