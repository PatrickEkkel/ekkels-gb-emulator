package core.parser;

import core.cpu.CPU;
import core.cpu.OpcodeDSL;
import core.cpu.Standard8BitDSL;
import core.cpu.opcodes.Decoder;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.OpcodeFactory;
import core.cpu.registers.Registers;
import core.mmu.Computable;
import core.mmu.MMU;
import core.mmu.MemoryAddress;

import java.util.ArrayList;
import java.util.List;

public class OpcodeConverter {

    private List<Opcode> opcodes = new ArrayList<>();
    private CPU cpu;
    private OpcodeFactory opcodeFactory;

    public OpcodeConverter(CPU cpu, MMU mmu) {
        this.cpu = cpu;
        Decoder [] decoders = this.cpu.getDecoders();
        List<Opcode> opcodes = new ArrayList<>();
        for(Decoder decoder : decoders) {
            opcodes.addAll(decoder.getOpcodes());
        }
        this.setOpcodes(opcodes);
        OpcodeDSL dsl = new Standard8BitDSL(mmu,cpu);
        opcodeFactory = new OpcodeFactory(dsl,mmu,cpu);
    }


    private void setOpcodes(List<Opcode> opcodes) {
        this.opcodes = opcodes;
    }



    private List<Computable> parseArguments(Mnemonic mnemonic) {

        List<Computable> result = new ArrayList<>();

        for(String argument : mnemonic.getArguments()) {
            if(ArgumentClassifier.is16BitValue(argument) || ArgumentClassifier.is8BitValue(argument)) {
                result.add(MemoryAddress.fromHexString(argument));
            }

            else if(ArgumentClassifier.isRegister(argument)) {
                result.add(this.cpu.readRegister(Registers.getRegister(argument)));
            }
            else if(ArgumentClassifier.is8BitSignedValue(argument)) {
                String signedArgument = argument.substring(1,argument.length());
                result.add(MemoryAddress.fromString(signedArgument));
            }
        }
        return result;
    }
    public Opcode getOpcode(String instruction) {
        for(Opcode opcode : this.opcodes) {
            if(opcode.toString().equals(instruction)) {
                return opcodeFactory.newOpcode(opcode.getClass());
            }
        }
        return null;
    }
    private int [] appendArray(int [] result, int [] instr, int pointer) {
        for(int i=0;i<instr.length;i++) {
            result[pointer] = instr[i];
            pointer++;
        }
        return result;
    }
    public int [] convert(List<String> instructions) {
        int [] result = new int[100];
        int pointer = 0;
        for(String instruction : instructions) {
            Mnemonic mnemonic = new Mnemonic(instruction);
            Opcode opcode = getOpcode(mnemonic.getInstruction());
            opcode.setComputables(this.parseArguments(mnemonic));
            if(opcode != null) {
               result = this.appendArray(result,opcode.toBinary(), pointer);
               pointer += opcode.toBinary().length;
            }
        }
        return result;
    }
}
