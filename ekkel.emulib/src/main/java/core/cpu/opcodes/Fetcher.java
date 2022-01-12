package core.cpu.opcodes;


import core.cpu.CPU;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.mmu.MMU;
import core.mmu.MMUImpl;
import core.mmu.MemoryAddress;
import core.mmu.MemoryValue;

public class Fetcher {
    private MMU mmuImpl;
    private Decoder decoder;
    private CPU cpu;
    private MemoryValue currentOpcode;


    public Fetcher(MMU mmuImpl, CPU cpu, Decoder decoder) {
        this.mmuImpl = mmuImpl;
        this.decoder = decoder;
        this.cpu = cpu;
    }


    protected MemoryValue getCurrentOpcode() {
        return this.currentOpcode;
    }

    protected int getPC() {
        return this.cpu.readRegister(Registers.PC).getValue();
    }


    public Decoder fetch() throws NotImplementedException, IllegalAccessException {
        this.currentOpcode  = mmuImpl.read(MemoryAddress.fromValue(getPC()));
        decoder.setOpcode(currentOpcode.getValue());
        return decoder;
    }
}
