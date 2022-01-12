package core.mmu.memorymap;

import core.mmu.MMUComponent;
import core.mmu.MemoryAddress;
import core.mmu.memorymap.exceptions.MemoryRegionDescriptionNotFound;

import java.util.ArrayList;
import java.util.List;

/**
 * Memory map to repres
 */
public class MemoryMap {

    private List<MemoryMapEntry> entryList;

    public MemoryMap() {
        this.entryList = new ArrayList<>();
    }

    public void addEntry(MMUComponent mmuComponent) {
        this.entryList.addAll(mmuComponent.getComponentIds());
    }

    public List<MemoryMapEntry> getEntryList() {
        return entryList;
    }

    public void merge(MemoryInterface memoryInterface) {
        MemoryMap memoryMap = memoryInterface.getMemoryMap();
        this.entryList.addAll(this.getEntryList());
    }
    public boolean isData(MemoryAddress memoryAddress) {
        boolean result = false;
        for(MemoryMapEntry entry : this.entryList) {
            if(entry.isInRange(memoryAddress)) {
                result = entry.isData();
                break;
            }
        }
        return result;
    }
    public String getMemoryRegionDescription(MemoryAddress memoryAddress) throws MemoryRegionDescriptionNotFound {
        String result = null;
        for(MemoryMapEntry entry : this.entryList) {
            if(entry.isInRange(memoryAddress)) {
                result = entry.getDescription();
            }
        }

        if(result == null) {
            throw new MemoryRegionDescriptionNotFound(memoryAddress);
        }

        return result;
    }


}
