package debugger.client.traceLogger;

import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.OpcodeFactory;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.MMU;
import core.mmu.MemoryAddress;
import ekkel.gameboy.cpu.opcodes.misc.NOP;
import gui.Palette;

import java.util.ArrayList;
import java.util.List;

public class OpcodePattern {
    private int offset;
    private List<Opcode> opcodes;

    private OpcodeFactory opcodeFactory;
    public OpcodePattern(OpcodeFactory opcodeFactory) {
        this.opcodes = new ArrayList<>();
        this.opcodeFactory = opcodeFactory;
        this.offset = 0;
    }

    public int getOffset() {
        return offset;
    }

    public List<Opcode> getOpcodes() {
        return this.opcodes;
    }

    public void addOpcode(Class clazz) {
        this.opcodes.add(this.opcodeFactory.newOpcode(clazz));
    }

    public boolean isPatternDetected(MMU mmu, int PC) {
        int increment = PC;
        boolean match = true;

        for(Opcode opcode : this.opcodes) {
            try {
                if(opcode.getInstr() != mmu.read(MemoryAddress.fromValue(increment)).getValue()) {
                    match = false;
                    break;
                }
                else {
                      opcode.dryRun();
                      int opcodeLength = opcode.toBinary().length;
                      increment += opcodeLength;
                      offset += opcodeLength;
                }
            } catch (NotImplementedException | IllegalAccessException e) {
                e.printStackTrace();
            }
        }
        return match;
    }



}
