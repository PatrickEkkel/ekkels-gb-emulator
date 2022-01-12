package core.cpu.opcodes;

import core.cpu.CPU;
import core.cpu.OpcodeDSL;
import core.mmu.MMU;
import core.mmu.MMUImpl;

public class OpcodeFactory {
    protected OpcodeDSL opcodeDSL;
    private MMU mmuImpl;
    private CPU cpu;

    public OpcodeFactory(OpcodeDSL dsl, MMU mmuImpl, CPU cpu) {
        this.opcodeDSL = dsl;
        this.mmuImpl = mmuImpl;
        this.cpu = cpu;
    }

    public Opcode newOpcode(Class clazz) {
        return Opcode.fromClass(clazz,cpu,this.opcodeDSL);
    }

}
