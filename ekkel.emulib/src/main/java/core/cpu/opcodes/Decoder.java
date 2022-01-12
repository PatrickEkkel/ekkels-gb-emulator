package core.cpu.opcodes;

import core.cpu.CPU;
import core.cpu.OpcodeDSL;
import core.cpu.opcodes.exceptions.UnknownOpcodeException;
import core.cpu.registers.Registers;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Decoder {

    protected Map<Integer,Opcode> opcodeMap= new HashMap<>();
    protected OpcodeDSL opcodeDSL;
    protected int opcode = 0x00;
    protected CPU cpu;
    public Decoder(CPU cpu) {
        this.cpu = cpu;
    }

    protected void addOpcode(Opcode opcode) {
        this.opcodeMap.put(opcode.getInstr(),opcode);
    }

    public void setOpcode(int opcode) {
        this.opcode =  opcode;
    }

    public int getOpcode() {
        return this.opcode;
    }

    public OpcodeDSL getOpcodeDSL() {
        return this.opcodeDSL;
    }

    public List<Opcode> getOpcodes() {
        return new ArrayList<>(opcodeMap.values());
    }

    public Opcode decode() throws UnknownOpcodeException {
        Opcode result  = this.opcodeMap.get(this.opcode);
        if(result == null)  {
            String pc = this.cpu.readRegister(Registers.PC).toString();
            throw  new UnknownOpcodeException(String.format("0x%s is an illigal opcode at %s ",Integer.toHexString(this.opcode),pc));
        }
        return new OpcodeExecutionWrapper(result);
    }
}
