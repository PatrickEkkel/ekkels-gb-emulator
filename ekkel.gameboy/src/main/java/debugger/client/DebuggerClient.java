package debugger.client;

import core.cpu.CPU;
import core.cpu.opcodes.exceptions.DivergedCPUStateException;
import core.mmu.MMUImpl;
import debugger.DebugOptions;

public interface DebuggerClient {

    void debug(CPU cpu);

    void printCPUState(CPU cpu);

    void printClockCycles(long clockCycles);

    void printRegisters(MMUImpl mmuImpl);

    void modifyCpuState(CPU cpu);

    void wrapUp() throws DivergedCPUStateException;

    DebugOptions getDebugOptions();

}
