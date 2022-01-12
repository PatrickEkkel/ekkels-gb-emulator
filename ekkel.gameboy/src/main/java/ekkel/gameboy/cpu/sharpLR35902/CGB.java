package ekkel.gameboy.cpu.sharpLR35902;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.MMUComponent;
import core.mmu.MemoryAddress;
import core.mmu.MemoryValue;
import core.mmu.memorymap.MemoryMapEntry;
import ekkel.gameboy.cpu.IOMap;

import java.util.ArrayList;
import java.util.List;

/**
 * CGB Registers, only applicable to CGB CPU, not implemented for now
 */
public class CGB extends MMUComponent {
    @Override
    public void write(MemoryAddress memoryAddress, MemoryValue value) throws NotImplementedException {
        // Ignore writes
    }

    @Override
    public MemoryValue read(MemoryAddress memoryAddress) throws NotImplementedException, IllegalAccessException {
        return MemoryValue.fromValue(0x7EFF);
        //return MemoryValue.fromValue(0xFFFF);
    }

    @Override
    public boolean IsAddressed(MemoryAddress memoryAddress) throws NotImplementedException {
        return memoryAddress.getValue() == IOMap.KEY1;
    }

    @Override
    public List<MemoryMapEntry> getComponentIds() {
        MemoryMapEntry memoryMapEntry = new MemoryMapEntry("CGB");
        memoryMapEntry.addRegister(IOMap.KEY1,"KEY 1");

        List<MemoryMapEntry> result = new ArrayList<>();
        result.add(memoryMapEntry);
        return result;
    }
}
