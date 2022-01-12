package core.mmu;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.memorymap.MemoryMap;

import java.util.ArrayList;
import java.util.List;

public class MMUImpl implements MMU {
    private MemoryMap memoryMap;
    private List<MMUComponent> components = new ArrayList<>();
    public MMUImpl() {
        this.memoryMap = new MemoryMap();
    }

    public void connect(MMUComponent mmuComponent) {
        memoryMap.addEntry(mmuComponent);
        components.add(mmuComponent);
    }

    public void disconnect(MMUComponent mmuComponent) { components.remove(mmuComponent); }

    @Override
    public MemoryMap getMemoryMap() {
        return this.memoryMap;
    }

    public void flush()  {
        this.components = new ArrayList<>();
    }

    public void write(MemoryAddress memoryAddress, MemoryValue memoryValue) throws NotImplementedException {

        for (MMUComponent mmuComponent : this.components) {
            if(mmuComponent.IsAddressed(memoryAddress))  {
                mmuComponent.write(memoryAddress,memoryValue);
                return;
            }
        }

    }
    public MemoryValue read(MemoryAddress memoryAddress) throws NotImplementedException, IllegalAccessException {
        for(MMUComponent mmuComponent : this.components) {
            if(mmuComponent.IsAddressed(memoryAddress)) {
                return mmuComponent.read(memoryAddress);
            }
        }
        throw  new IllegalAccessException(String.format("Trying to access memory address that is illigal %s", memoryAddress.getValue() ));
    }

}
