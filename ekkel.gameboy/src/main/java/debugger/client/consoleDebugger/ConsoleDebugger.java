package debugger.client.consoleDebugger;

import core.cpu.CPU;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.opcodes.exceptions.UnknownOpcodeException;
import core.cpu.registers.Registers;
import core.mmu.MMUImpl;
import core.mmu.MemoryAddress;
import debugger.DebugOptions;
import debugger.client.DebuggerClient;

public class ConsoleDebugger implements DebuggerClient {

    DebugOptions debugOptions;
    public ConsoleDebugger(DebugOptions options) {
        this.debugOptions = options;
    }

    @Override
    public void debug(CPU cpu) {
        String debugLine = "";
        if(this.debugOptions.isEmitProgramCounter()) {
            debugLine += cpu.readRegister(Registers.PC).toString();
        }

        if(this.debugOptions.isEmitCurrentOpcode()) {
            try {
                Opcode opcode = cpu.getFetcher().fetch().decode();
                opcode.dryRun();
                debugLine += " " + opcode.toString();

            } catch (UnknownOpcodeException | NotImplementedException | IllegalAccessException e) {
                e.printStackTrace();
            }
        }

        System.out.println(debugLine);
    }

    @Override
    public void printCPUState(CPU cpu) {

        if(debugOptions.isEmitRegisters()) {
            System.out.printf("AF %s%n",cpu.readRegister(Registers.AF));
            System.out.printf("BC %s%n",cpu.readRegister(Registers.BC));
            System.out.printf("DE %s%n",cpu.readRegister(Registers.DE));
            System.out.printf("HL %s%n",cpu.readRegister(Registers.HL));
            System.out.printf("SP %s%n",cpu.readRegister(Registers.SP));
        }

    }

    @Override
    public void printClockCycles(long clockCycles) {
        if(debugOptions.isEmitClockcycles()) {
            System.out.println(String.format("clockycles: %s", clockCycles));
        }
    }

    @Override
    public void printRegisters(MMUImpl mmuImpl) {

        try {
            if(debugOptions.isEmitExternalRegisters()) {
                System.out.println(String.format("FF44 (LY): %s", mmuImpl.read(MemoryAddress.fromValue(0xFF44)).toString()));
            }
        } catch (NotImplementedException | IllegalAccessException e) {
            e.printStackTrace();
        }

    }

    @Override
    public void modifyCpuState(CPU cpu) {

    }

    @Override
    public void wrapUp() {
        if(this.debugOptions.isEnableDebug()) {
            System.out.println("------------------------------------------------");
        }
    }

    @Override
    public DebugOptions getDebugOptions() {
        return this.debugOptions;
    }


}
