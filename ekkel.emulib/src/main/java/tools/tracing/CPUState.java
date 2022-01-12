package tools.tracing;

import core.cpu.registers.Register;

import java.util.HashMap;
import java.util.Map;

public class CPUState {

    private int pc;
    private int opcode;
    private int opcodeCounter;
    private Map<String, Register> registers;

    public CPUState(int pc, int opcode, int opcodeCounter) {
        this.pc = pc;
        this.opcode = opcode;
        this.opcodeCounter = opcodeCounter;
        this.registers = new HashMap<>();
    }

    public int getOpcode() {
        return opcode;
    }

    public void setOpcode(int opcode) {
        this.opcode = opcode;
    }

    public int getPc() {
        return pc;
    }

    public void setPc(int pc) {
        this.pc = pc;
    }

    public void setRegisters(Map<String, Register> registers) {
        this.registers = registers;
    }

    public Map<String, Register> getRegisters() {
        return this.registers;
    }

    public int getOpcodeCounter() {
        return opcodeCounter;
    }

    public void setOpcodeCounter(int opcodeCounter) {
        this.opcodeCounter = opcodeCounter;
    }
}
