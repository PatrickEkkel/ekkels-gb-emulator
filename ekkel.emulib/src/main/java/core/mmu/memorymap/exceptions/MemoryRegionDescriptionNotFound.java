package core.mmu.memorymap.exceptions;

import core.mmu.MemoryAddress;

public class MemoryRegionDescriptionNotFound extends Exception {
    public MemoryRegionDescriptionNotFound(MemoryAddress address) {
        super(String.format("Description for address %s not found", address));
    }

}
