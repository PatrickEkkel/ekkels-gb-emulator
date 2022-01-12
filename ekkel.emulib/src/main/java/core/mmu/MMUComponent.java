package core.mmu;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.memorymap.MemoryMapEntry;

import java.util.List;

/**
 * Allows to connect devices to the memory mapped IO of the CPU
 */
public abstract class MMUComponent {
    public abstract void write(MemoryAddress memoryAddress, MemoryValue value) throws NotImplementedException;
    public abstract MemoryValue read(MemoryAddress memoryAddress) throws NotImplementedException, IllegalAccessException;
    public abstract boolean IsAddressed(MemoryAddress memoryAddress) throws NotImplementedException;
    public abstract List<MemoryMapEntry> getComponentIds();
}
