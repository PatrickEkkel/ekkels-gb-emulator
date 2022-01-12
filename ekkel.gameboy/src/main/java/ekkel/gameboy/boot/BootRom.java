package ekkel.gameboy.boot;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.MMUComponent;
import core.mmu.MemoryAddress;
import core.mmu.MemoryValue;
import core.rom.Rom;
import core.rom.RomLoader;
import ekkel.gameboy.cpu.IOMap;

public class BootRom extends Rom {

    private BootRomLoader loader;

    public BootRom() {

    }

    public void setBootRomLoader(BootRomLoader loader) {
        this.loader = loader;
    }

    @Override
    public void write(MemoryAddress memoryAddress, MemoryValue value) {
        // Sanity check, this is the only address allowed to write to the rom
        if(memoryAddress.getValue() == IOMap.DMGROMDISABLE && value.getValue() == 0x01) {
            // unmap the bootrom, all reads will now be redirected to the cartridge
            this.loader.unMap();
        }
    }

    @Override
    public MemoryValue read(MemoryAddress memoryAddress)  {
        return MemoryValue.fromByte(this.getRomContents()[memoryAddress.getValue()]);
    }

    @Override
    public boolean IsAddressed(MemoryAddress memoryAddress)  {
        return (memoryAddress.getValue() >= 0x00 && memoryAddress.getValue() < 0x100) || memoryAddress.getValue() == 0xFF50;
    }
}
