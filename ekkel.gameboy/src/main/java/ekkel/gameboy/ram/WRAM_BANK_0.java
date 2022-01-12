package ekkel.gameboy.ram;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.MMUComponent;
import core.mmu.MemoryAddress;
import core.mmu.MemoryValue;
import core.mmu.memorymap.MemoryMapEntry;

import java.util.ArrayList;
import java.util.List;

public class WRAM_BANK_0  extends MMUComponent {

    protected final int WRAM_BANK_0_START = 0xC000;
    protected final int WRAM_BANK_0_END = 0xCFFF;
    private int [] ram;


    public WRAM_BANK_0() {
        this.ram = new int[WRAM_BANK_0_END+1];
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
        return memoryAddress.getValue() >= WRAM_BANK_0_START && memoryAddress.getValue() <= WRAM_BANK_0_END;
    }

    @Override
    public List<MemoryMapEntry> getComponentIds() {

        List<MemoryMapEntry> memoryMapEntries = new ArrayList<>();

        memoryMapEntries.add(new MemoryMapEntry(WRAM_BANK_0_START,WRAM_BANK_0_END,"WRAM0"));
        return memoryMapEntries;
    }
}
