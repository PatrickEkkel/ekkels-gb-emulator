package core.rom;

import core.mmu.MemoryAddress;
import core.mmu.MMUComponent;
import core.mmu.MemoryValue;
import core.mmu.memorymap.MemoryMapEntry;

import java.util.ArrayList;
import java.util.List;

public class Rom extends MMUComponent {

    private byte[] romContents;

    public void setRomContents(byte [] romContents) {
        this.romContents = romContents;
    }

    protected byte[] getRomContents() {
        return this.romContents;
    }

    @Override
    public void write(MemoryAddress memoryAddress, MemoryValue value) {

    }

    @Override
    public MemoryValue read(MemoryAddress memoryAddress) {
        return MemoryValue.empty();
    }

    @Override
    public boolean IsAddressed(MemoryAddress memoryAddress) {
        return false;
    }

    @Override
    public List<MemoryMapEntry> getComponentIds() {
        List<MemoryMapEntry> memoryMapEntries = new ArrayList<>();
        memoryMapEntries.add(new MemoryMapEntry(0x104,0x133,"HLOGO") {
            @Override
            public boolean isData() {
                return true;
            }
        });
        memoryMapEntries.add(new MemoryMapEntry(0x134, 0x143,"HTITLE") {
            @Override
            public boolean isData() {
                return true;
            }
        });
        memoryMapEntries.add(new MemoryMapEntry(0x144,0x145,"HLICENCE") {
            @Override
            public boolean isData() {
                return true;
            }
        });
        memoryMapEntries.add(new MemoryMapEntry(0x0000,0x3FFF,"ROM0"));
        memoryMapEntries.add(new MemoryMapEntry(0x4000,0x7FFF,"ROM1"));
        return memoryMapEntries;
    }
}
