package ekkel.gameboy.interrupts;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.MMUComponent;
import core.mmu.MemoryAddress;
import core.mmu.MemoryValue;
import core.mmu.memorymap.MemoryMap;
import core.mmu.memorymap.MemoryMapEntry;
import ekkel.gameboy.cpu.IOMap;

import java.util.ArrayList;
import java.util.List;

public class InterruptFlag extends MMUComponent {

    private int interruptFlag = IOMap.IE;


    @Override
    public void write(MemoryAddress memoryAddress, MemoryValue value) {
        this.interruptFlag = value.getValue();
    }

    @Override
    public MemoryValue read(MemoryAddress memoryAddress) throws NotImplementedException, IllegalAccessException {
        return MemoryValue.fromValue(this.interruptFlag);
    }

    @Override
    public boolean IsAddressed(MemoryAddress memoryAddress) throws NotImplementedException {
        return memoryAddress.getValue() == IOMap.IE;
    }

    @Override
    public List<MemoryMapEntry> getComponentIds() {

        MemoryMapEntry memoryMapEntry = new MemoryMapEntry("Interrupts");
        memoryMapEntry.addRegister(IOMap.IE, "IE (interrupt enabled)");

        List<MemoryMapEntry> memoryMapEntries = new ArrayList<>();
        memoryMapEntries.add(memoryMapEntry);
        return memoryMapEntries;
    }
}
