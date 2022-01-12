package ekkel.gameboy.rom;

import core.mmu.MemoryAddress;
import core.mmu.MemoryValue;
import core.rom.Rom;

public class TestRom extends GameboyRom {

    private int [] testRom;

    public TestRom(int [] testRom) {
        this.testRom = testRom;

        byte[] contents = new byte[this.CARTRIDGE_ROM_00_END];
        for(int i=0;i<testRom.length;i++) {
            contents[i] = (byte) testRom[i];
        }
        this.setRomContents(contents);

    }

    @Override
    public void write(MemoryAddress memoryAddress, MemoryValue value) {
    }
}
