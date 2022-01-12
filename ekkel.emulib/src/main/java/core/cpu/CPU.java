package core.cpu;

import core.cpu.opcodes.Decoder;
import core.cpu.opcodes.Fetcher;
import core.cpu.opcodes.exceptions.DivergedCPUStateException;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.opcodes.exceptions.UnknownOpcodeException;
import core.cpu.registers.Register;
import core.cpu.registers.Registers;
import core.mmu.Computable;
import core.mmu.MMUComponent;
import core.mmu.memorymap.MemoryInterface;

import java.util.HashMap;
import java.util.Map;

public abstract class CPU extends MMUComponent implements CPU8Bit, MemoryInterface {

    protected Stack stack;
    protected Map<Registers, Register> reg = new HashMap<>();

    public CPU() {
        defineRegisters();

    }

    protected abstract void defineRegisters();

    public abstract void initRegisterStartValues();

    public abstract Decoder [] getDecoders();

    public abstract Fetcher getFetcher();

    public abstract void setFetcher(Fetcher fetcher);

    public Map<Registers,Register> getReg() {
        return this.reg;
    }

    public void setPC(int value) {
        this.reg.get(Registers.PC).setValue(value);
    }

    public int getPC() {
        return this.reg.get(Registers.PC).getValue();
    }


    public Stack getStack() {
        return this.stack;
    }



    public Register readRegister(Registers key) {
        return this.reg.get(key);
    }

    public void writeRegister(Registers key, Computable value) {
        Register selectedRegister = reg.get(key);

        if(selectedRegister.getBits() == 8 && value.is16Bit()) {
            reg.get(key).setValue(value.getHighByte());
        }
        else {
            reg.get(key).setValue(value.getValue());
        }

    }


    public int tick(long cycles) throws NotImplementedException, IllegalAccessException, UnknownOpcodeException, DivergedCPUStateException {
        return 0;

    }

}
