import core.cpu.registers.Register;
import core.cpu.registers.Registers;
import core.mmu.MMUImpl;
import core.parser.OpcodeConverter;
import ekkel.gameboy.Gameboy;
import ekkel.gameboy.TestBoy;
import ekkel.gameboy.cpu.sharpLR35902.SharpLR35902;
import core.cpu.flags.utils.FlagsHelper;

import static org.junit.jupiter.api.Assertions.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class OpcodeTestBase {

    private void clearMMU() {

    }

    public TestBoy createTestContext(int pc, int limit, String... program) {
        List<String> instructions = new ArrayList<>(Arrays.asList(program));
        return this.setupTest(instructions, pc, limit);
    }

    private TestBoy setupTest(List<String> instructions, int pc, int limit) {
        MMUImpl mmuImpl = new MMUImpl();
        SharpLR35902 cpu = new SharpLR35902(mmuImpl, false);
        TestBoy gameboy = new TestBoy(pc, limit);
        OpcodeConverter opcodeConverter = new OpcodeConverter(cpu, gameboy.getMMU());
        int[] program = opcodeConverter.convert(instructions);
        gameboy.load(program);
        return gameboy;
    }

    public void testFlags(Gameboy context, int actual, int expected) {
        FlagsHelper actualFlags = new FlagsHelper(context.getCPU(), new Register(actual, 8, Registers.F));
        FlagsHelper expectedFlags = new FlagsHelper(context.getCPU(), new Register(expected, 8, Registers.F));

        assertEquals(expectedFlags.isZ(), actualFlags.isZ(),"Zero");
        assertEquals(actualFlags.isN(), expectedFlags.isN(),"Substract");
        assertEquals(actualFlags.isC(), expectedFlags.isC(), "Carry");
        assertEquals(actualFlags.isH(), expectedFlags.isH(),"Halfcarry");
    }

}
