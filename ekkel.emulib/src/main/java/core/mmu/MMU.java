package core.mmu;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.memorymap.MemoryInterface;
import core.mmu.memorymap.MemoryMap;

public interface MMU extends MemoryInterface {

    void write(MemoryAddress memoryAddress, MemoryValue memoryValue)  throws NotImplementedException;
    MemoryValue read(MemoryAddress memoryAddress) throws NotImplementedException, IllegalAccessException;
    void flush();
    void connect(MMUComponent mmuComponent);
    void disconnect(MMUComponent mmuComponent);
}
