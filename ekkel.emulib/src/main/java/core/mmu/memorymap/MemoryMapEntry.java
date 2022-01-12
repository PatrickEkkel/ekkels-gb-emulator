package core.mmu.memorymap;

import core.mmu.MemoryAddress;

import java.util.HashMap;
import java.util.List;

public class MemoryMapEntry {

    private int start;
    private int end;
    private boolean header;
    private HashMap<Integer, String> registers;

    private String description;

    public MemoryMapEntry() {
        this.registers = new HashMap<>();
    }
    public MemoryMapEntry(String description) {
        this();
        this.description = description;
    }

    public MemoryMapEntry(int start, int end, String description) {
        this(description);
        this.start = start;
        this.end = end;
        this.description = description;
    }

    public boolean isInRange(MemoryAddress memoryValue) {
        boolean result = false;
        if (!registers.isEmpty()) {

            for (int key : this.registers.keySet()) {
                if (key == memoryValue.getValue()) {
                    result = true;
                    break;
                }
            }
        } else if(memoryValue.getValue() >= this.start && memoryValue.getValue() <= this.end) {
            result = true;
        }
        return result;
    }
    public void setHeader(boolean header) {
        this.header = header;
    }
    public boolean isData() {
        return this.header;
    }

    public void addRegister(Integer register, String description) {
        this.registers.put(register, description);
    }

    public HashMap<Integer, String> getRegisters() {
        return this.registers = new HashMap<>();
    }


    public boolean hasRegisters() {
        return !this.registers.isEmpty();
    }

    public String getDescription() {
        return this.description;
    }

    public int getStart() {
        return this.start;
    }

    public int getEnd() {
        return this.end;
    }
}
