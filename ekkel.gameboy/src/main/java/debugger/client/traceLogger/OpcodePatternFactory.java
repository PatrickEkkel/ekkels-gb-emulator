package debugger.client.traceLogger;

import core.cpu.OpcodeDSL;
import core.cpu.Standard8BitDSL;
import core.cpu.opcodes.OpcodeFactory;
import ekkel.gameboy.Gameboy;

public class OpcodePatternFactory {
    private OpcodeDSL dsl;
    private Gameboy gameboy;
    public OpcodePatternFactory(Gameboy gameboy) {
        this.gameboy = gameboy;
        this.dsl = new Standard8BitDSL( gameboy.getMMU(),gameboy.getCPU());
    }
    public OpcodePattern create() {
        OpcodeFactory opcodeFactory = new OpcodeFactory(this.dsl,this.gameboy.getMMU(),this.gameboy.getCPU());
        return new OpcodePattern(opcodeFactory);
    }

}
