package ekkel.gameboy.ppu.vram;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.MMUComponent;
import core.mmu.MemoryAddress;
import core.mmu.MemoryValue;
import core.mmu.memorymap.MemoryMapEntry;

import java.util.ArrayList;
import java.util.List;

public class VRAM extends MMUComponent  {

    protected final int VRAM_START = 0x8000;
    protected final int VRAM_END = 0x9FFF;

    private int [] vram;

    public VRAM() {
        this.vram = new int[VRAM_END+1];
    }

    @Override
    public void write(MemoryAddress memoryAddress, MemoryValue value) throws NotImplementedException {
        this.vram[memoryAddress.getValue()] = value.getValue();
    }

    @Override
    public MemoryValue read(MemoryAddress memoryAddress) throws NotImplementedException, IllegalAccessException {
        return MemoryValue.fromValue(this.vram[memoryAddress.getValue()]);
    }

    @Override
    public boolean IsAddressed(MemoryAddress memoryAddress) throws NotImplementedException {
        return  memoryAddress.getValue() >= VRAM_START && memoryAddress.getValue() <= VRAM_END;
    }

    @Override
    public List<MemoryMapEntry> getComponentIds() {
        List<MemoryMapEntry> memoryMapEntries = new ArrayList<>();
        memoryMapEntries.add(new MemoryMapEntry(VRAM_START, VRAM_END,"VRAM") {
            @Override
            public boolean isData() {
                return true;
            }
        });
        return memoryMapEntries;
    }
}
