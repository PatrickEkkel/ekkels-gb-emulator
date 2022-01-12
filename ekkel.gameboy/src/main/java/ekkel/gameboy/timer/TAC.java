package ekkel.gameboy.timer;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.MMUComponent;
import core.mmu.MemoryAddress;
import core.mmu.MemoryValue;
import core.mmu.memorymap.MemoryMapEntry;
import ekkel.gameboy.cpu.IOMap;

import java.util.ArrayList;
import java.util.List;

/**
 * Timer Control, Not fully implemented. just read write for now
 *
 * Bit  2   - Timer Enable
 * Bits 1-0 - Input Clock Select
 *            00: CPU Clock / 1024 (DMG, SGB2, CGB Single Speed Mode:   4096 Hz, SGB1:   ~4194 Hz, CGB Double Speed Mode:   8192 Hz)
 *            01: CPU Clock / 16   (DMG, SGB2, CGB Single Speed Mode: 262144 Hz, SGB1: ~268400 Hz, CGB Double Speed Mode: 524288 Hz)
 *            10: CPU Clock / 64   (DMG, SGB2, CGB Single Speed Mode:  65536 Hz, SGB1:  ~67110 Hz, CGB Double Speed Mode: 131072 Hz)
 *            11: CPU Clock / 256  (DMG, SGB2, CGB Single Speed Mode:  16384 Hz, SGB1:  ~16780 Hz, CGB Double Speed Mode:  32768 Hz)
 */
public class TAC extends MMUComponent {
    private int tac;

    @Override
    public void write(MemoryAddress memoryAddress, MemoryValue value) throws NotImplementedException {
        this.tac = value.getValue();
    }

    @Override
    public MemoryValue read(MemoryAddress memoryAddress) throws NotImplementedException, IllegalAccessException {
        return MemoryValue.fromValue(this.tac);
    }

    @Override
    public boolean IsAddressed(MemoryAddress memoryAddress) throws NotImplementedException {
        return memoryAddress.getValue() == IOMap.TAC;
    }

    @Override
    public List<MemoryMapEntry> getComponentIds() {
        MemoryMapEntry memoryMapEntry = new MemoryMapEntry("TAC");
        memoryMapEntry.addRegister(IOMap.TAC,"Timer");

        List<MemoryMapEntry> memoryMapEntries = new ArrayList<>();
        memoryMapEntries.add(memoryMapEntry);
        return memoryMapEntries;
    }
}
