import core.cpu.CPU;
import core.cpu.Flags;
import core.cpu.OpcodeDSL;
import core.cpu.Standard8BitDSL;
import core.cpu.opcodes.OpcodeFactory;
import core.cpu.registers.Registers;
import core.mmu.MMUImpl;
import core.mmu.MemoryValue;
import ekkel.gameboy.Gameboy;
import org.junit.jupiter.api.Test;

public class CPUFlagTests extends OpcodeTestBase {

    public class TestOpcodeFactory extends OpcodeFactory {
        public TestOpcodeFactory(OpcodeDSL dsl, MMUImpl mmuImpl, CPU cpu) {
            super(dsl, mmuImpl, cpu);
        }

        public OpcodeDSL getDsl() {
            return this.opcodeDSL;
        }
    }

    private TestOpcodeFactory createOpcodeFactory(Gameboy gameboy) {


        return new TestOpcodeFactory(
                new Standard8BitDSL(gameboy.getMMU(),
                                    gameboy.getCPU()),
                                    gameboy.getMMU(),
                                    gameboy.getCPU());

    }
    @Test
    public void testSetZeroFlag() {
        Gameboy gameboy = this.createTestContext(0x00,0x10,"NOP");

         TestOpcodeFactory factory = createOpcodeFactory(gameboy);
        OpcodeDSL dsl = factory.getDsl();
        gameboy.getCPU().writeRegister(Registers.A, MemoryValue.fromValue(0x01));
        gameboy.getCPU().writeRegister(Registers.F,MemoryValue.fromValue(0x00));
        dsl.load(Registers.A).dec().flags(Flags.Z,0,0,0);
        assert gameboy.getCPU().readRegister(Registers.F).getValue() == 0x80;
    }
    @Test
    public void testClearZeroFlag() {
        Gameboy gameboy = this.createTestContext(0x00,0x10,"NOP");

        TestOpcodeFactory factory = createOpcodeFactory(gameboy);
        OpcodeDSL dsl = factory.getDsl();
        gameboy.getCPU().writeRegister(Registers.A, MemoryValue.fromValue(0x20));
        gameboy.getCPU().writeRegister(Registers.F,MemoryValue.fromValue(0x00));
        dsl.load(Registers.A).dec().flags(Flags.Z,0,0,0);
        assert gameboy.getCPU().readRegister(Registers.F).getValue() == 0x00;
    }
    @Test
    public void testSetToClearZeroFlag() {
        Gameboy gameboy = this.createTestContext(0x00,0x10,"NOP");

        TestOpcodeFactory factory = createOpcodeFactory(gameboy);
        OpcodeDSL dsl = factory.getDsl();
        gameboy.getCPU().writeRegister(Registers.A, MemoryValue.fromValue(0x20));
        gameboy.getCPU().writeRegister(Registers.F,MemoryValue.fromValue(0x80));
        dsl.load(Registers.A).dec().flags(Flags.Z,0,0,0);
        assert gameboy.getCPU().readRegister(Registers.F).getValue() == 0x00;
    }


}
