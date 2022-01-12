package ekkel.gameboy.serial;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.MMUComponent;
import core.mmu.MemoryAddress;
import core.mmu.MemoryValue;
import core.mmu.memorymap.MemoryMapEntry;
import debugger.SerialDevice;
import ekkel.gameboy.cpu.IOMap;

import java.util.ArrayList;
import java.util.List;

public class SerialPort extends MMUComponent {

    MemoryValue sb = null;
    SerialDevice serialDevice;

    public SerialPort(SerialDevice device) {
        this.serialDevice = device;
    }


    @Override
    public void write(MemoryAddress memoryAddress, MemoryValue value) throws NotImplementedException {

        if (memoryAddress.getValue() == IOMap.SC) {
            if (sb != null) {
                String data = String.format("%c", sb.getValue());
                this.serialDevice.logData(data);
            }
        } else if (memoryAddress.getValue() == IOMap.SB) {
            sb = value;
        }
    }

    @Override
    public MemoryValue read(MemoryAddress memoryAddress) throws NotImplementedException, IllegalAccessException {
        return MemoryValue.fromValue(0xFFFF);
    }

    @Override
    public boolean IsAddressed(MemoryAddress memoryAddress) throws NotImplementedException {
        return memoryAddress.getValue() == IOMap.SC || memoryAddress.getValue() == IOMap.SB;
    }

    @Override
    public List<MemoryMapEntry> getComponentIds() {
        List<MemoryMapEntry> memoryMapEntries = new ArrayList<>();
        MemoryMapEntry memoryMapEntry = new MemoryMapEntry("Serial");
        memoryMapEntry.addRegister(IOMap.SB, "Serial SB");
        memoryMapEntry.addRegister(IOMap.SC, "Serial SC");
        memoryMapEntries.add(memoryMapEntry);
        return memoryMapEntries;
    }
}
