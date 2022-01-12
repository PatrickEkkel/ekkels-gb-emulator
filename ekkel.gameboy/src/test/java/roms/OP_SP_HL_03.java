package roms;

import java.io.IOException;

public class OP_SP_HL_03 extends BlarggTestRom {

    public OP_SP_HL_03() throws IOException {
        String filename = "03-op sp,hl.gb";
        this.load(filename);
    }
}
