package ekkel.gameboy.rom;

import core.mmu.MemoryAddress;
import core.mmu.MemoryValue;
import core.rom.Rom;

public class GameboyRom extends Rom {

    protected final int CARTRIDGE_ROM_00_START = 0x0000;
    protected final int CARTRIDGE_ROM_00_END = 0x3FFF;

    protected final int CARTRIDGE_ROM_01_START = 0x4000;
    protected final int CARTRIDGE_ROM_01_END = 0x7FFF;

    @Override
    public boolean IsAddressed(MemoryAddress memoryAddress) {
        int value = memoryAddress.getValue();
        return ((value >= CARTRIDGE_ROM_00_START && value <= CARTRIDGE_ROM_00_END) ||
                (value >= CARTRIDGE_ROM_01_START && value <= CARTRIDGE_ROM_01_END));
    }

    @Override
    public MemoryValue read(MemoryAddress memoryAddress) {
        return MemoryValue.fromByte(this.getRomContents()[memoryAddress.getValue()]);
    }
}
