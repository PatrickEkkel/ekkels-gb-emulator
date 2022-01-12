package debugger;

import core.cpu.CPU;
import core.cpu.Clock;
import core.cpu.opcodes.Decoder;
import core.cpu.opcodes.Fetcher;
import core.cpu.opcodes.exceptions.DivergedCPUStateException;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.opcodes.exceptions.UnknownOpcodeException;
import core.cpu.registers.Registers;
import core.mmu.Computable;
import core.mmu.MMUImpl;
import core.mmu.MemoryAddress;
import core.mmu.MemoryValue;
import core.mmu.memorymap.MemoryMap;
import core.mmu.memorymap.MemoryMapEntry;
import debugger.client.DebuggerClient;

import java.util.List;

public class DebuggerBridge extends CPU {
    private CPU cpu;
    private MMUImpl mmuImpl;
    private DebuggerClient client;
    private Clock clock;
    private CPUInit cpuInit;


    public DebuggerBridge(CPU cpu, DebuggerClient client, Clock clock, MMUImpl mmuImpl) {
        this.cpu = cpu;
        this.reg = cpu.getReg();
        this.client = client;
        this.clock = clock;
        this.mmuImpl = mmuImpl;
    }

    public void setCpuInit(CPUInit cpuInit) {
        this.cpuInit = cpuInit;
    }

    @Override
    protected void defineRegisters() {

    }

    @Override
    public void initRegisterStartValues() {
        if(this.cpuInit != null) {
            this.cpuInit.doInit(this.cpu);
        }
        else {
            this.cpu.initRegisterStartValues();
        }
    }

    @Override
    public Decoder [] getDecoders() {
        return this.cpu.getDecoders();
    }

    @Override
    public Fetcher getFetcher() {

        if (!this.client.getDebugOptions().isDisableCpu()) {
            return this.cpu.getFetcher();
        }
        return new NOOPFetcher(mmuImpl, cpu);
    }

    @Override
    public void setFetcher(Fetcher fetcher) {

    }

    @Override
    public Computable getZeroFlag() {
        return this.cpu.getZeroFlag();
    }

    @Override
    public Computable getSubstractFlag() {
        return this.cpu.getSubstractFlag();
    }

    @Override
    public Computable getHalfCarryFlag() {
        return this.getHalfCarryFlag();
    }

    @Override
    public Computable getCarryFlag() {
        return this.getCarryFlag();
    }

    @Override
    public void setFlag(Computable flag) {
        this.cpu.setFlag(flag);
    }

    @Override
    public void write(MemoryAddress memoryAddress, MemoryValue value) throws NotImplementedException {
        this.cpu.write(memoryAddress,value);
    }

    @Override
    public MemoryValue read(MemoryAddress memoryAddress) throws NotImplementedException, IllegalAccessException {
        return this.cpu.read(memoryAddress);
    }

    @Override
    public boolean IsAddressed(MemoryAddress memoryAddress) throws NotImplementedException {
        return this.cpu.IsAddressed(memoryAddress);
    }

    @Override
    public List<MemoryMapEntry> getComponentIds() {
        return this.cpu.getComponentIds();
    }

    @Override
    public int tick(long cycles) throws NotImplementedException, IllegalAccessException, UnknownOpcodeException, DivergedCPUStateException {
        int result = 0;
        int PC = this.cpu.readRegister(Registers.PC).getValue();
        this.cpu.setFetcher(this.getFetcher());

        if(this.client.getDebugOptions().isEnableDebug()) {

            if (this.client.getDebugOptions().getBreakPoints().isEmpty()) {
                this.client.debug(this.cpu);
                this.client.printCPUState(this.cpu);
                this.client.printRegisters(this.mmuImpl);
                this.client.modifyCpuState(this.cpu);
                this.client.wrapUp();
            }

            for (BreakPoint breakPoint : this.client.getDebugOptions().getBreakPoints()) {
                if (breakPoint.getValue() == PC) {
                    this.client.debug(this.cpu);
                    this.client.printCPUState(this.cpu);
                    this.client.printRegisters(this.mmuImpl);
                    this.client.modifyCpuState(this.cpu);
                    this.client.wrapUp();
                }
            }
            if (this.client.getDebugOptions().isEmitClockcycles()) {
                this.client.printClockCycles(this.clock.getCycle());
            }
        }
        result = this.cpu.tick(cycles);
        return result;
    }

    @Override
    public MemoryMap getMemoryMap() {
        return this.cpu.getMemoryMap();
    }
}
