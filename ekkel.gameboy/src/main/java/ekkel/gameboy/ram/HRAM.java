package ekkel.gameboy.ram;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.MMUComponent;
import core.mmu.MemoryAddress;
import core.mmu.MemoryValue;
import core.mmu.memorymap.MemoryMapEntry;

import java.util.ArrayList;
import java.util.List;

public class HRAM extends MMUComponent {

    protected final int HRAM_START = 0xFF80;
    protected final int HRAM_END = 0xFFFE;
    private int [] ram;



    public HRAM() {
        this.ram = new int[HRAM_END+1];
    }

    @Override
    public void write(MemoryAddress memoryAddress, MemoryValue value) throws NotImplementedException {
        this.ram[memoryAddress.getValue()] = value.getValue();
    }

    @Override
    public MemoryValue read(MemoryAddress memoryAddress) throws NotImplementedException, IllegalAccessException {
        return MemoryValue.fromValue(this.ram[memoryAddress.getValue()]);
    }

    @Override
    public boolean IsAddressed(MemoryAddress memoryAddress) throws NotImplementedException {
        return memoryAddress.getValue() >= HRAM_START && memoryAddress.getValue() <= HRAM_END;
    }

    @Override
    public List<MemoryMapEntry> getComponentIds() {

        List<MemoryMapEntry> memoryMapEntries = new ArrayList<>();
        memoryMapEntries.add(new MemoryMapEntry(HRAM_START,HRAM_END,"HRAM"));
        return memoryMapEntries;
    }
}
