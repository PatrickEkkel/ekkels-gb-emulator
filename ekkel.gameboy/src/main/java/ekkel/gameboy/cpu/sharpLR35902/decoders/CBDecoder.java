package ekkel.gameboy.cpu.sharpLR35902.decoders;

import core.cpu.CPU;
import core.cpu.Standard8BitDSL;
import core.cpu.opcodes.Decoder;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.OpcodeFactory;
import core.cpu.opcodes.exceptions.UnknownOpcodeException;
import core.cpu.registers.Registers;
import core.mmu.MMU;
import ekkel.gameboy.cpu.opcodes.cb.*;
import ekkel.gameboy.cpu.opcodes.misc.NOP;

public class CBDecoder extends Decoder {
    public CBDecoder(CPU cpu, MMU mmuImpl) {
        super(cpu);
        this.opcodeDSL = new Standard8BitDSL(mmuImpl, cpu);
        OpcodeFactory opcodeFactory = new OpcodeFactory(this.opcodeDSL, mmuImpl,cpu);   this.addOpcode(opcodeFactory.newOpcode(NOP.class));
        this.addOpcode(opcodeFactory.newOpcode(SRL_A.class));
        this.addOpcode(opcodeFactory.newOpcode(SRL_B.class));

        this.addOpcode(opcodeFactory.newOpcode(RR_C.class));
        this.addOpcode(opcodeFactory.newOpcode(RR_D.class));
        this.addOpcode(opcodeFactory.newOpcode(RR_E.class));
        this.addOpcode(opcodeFactory.newOpcode(RL_C.class));

        this.addOpcode(opcodeFactory.newOpcode(SWAP_A.class));

        this.addOpcode(opcodeFactory.newOpcode(BIT_6_A.class));
        this.addOpcode(opcodeFactory.newOpcode(BIT_7_B.class));
    }

    @Override
    public Opcode decode() throws UnknownOpcodeException {

        try {
            return super.decode();
        }
        catch (UnknownOpcodeException ex) {
            String pc = this.cpu.readRegister(Registers.PC).toString();
            throw  new UnknownOpcodeException(String.format("0x%s is an illigal CB opcode at %s ",Integer.toHexString(this.getOpcode()),pc));

        }
    }
}
