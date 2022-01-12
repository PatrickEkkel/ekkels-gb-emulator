import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import roms.LD_R_R_06;
import roms.OP_R_IMM_04;
import roms.OP_SP_HL_03;
import testrunner.GameBoyRunner;

import java.io.IOException;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class BlarggTestRoms extends TestRomBase {

    @BeforeEach
    public void testTestFramework() throws IOException, InterruptedException {
        this.setupTest();
    }

    @Test
    public void test_04_OP_R_IMM() throws IOException {
        GameBoyRunner gameBoyRunner = new GameBoyRunner();
        gameBoyRunner.setRom(new OP_R_IMM_04());
        gameBoyRunner.setSerialDevice(this);
        gameBoyRunner.start();
        assertTrue(this.isTestPassed(gameBoyRunner));
    }

    @Test
    public void test_03_OP_SP_HL() throws IOException {
        GameBoyRunner gameBoyRunner = new GameBoyRunner();
        gameBoyRunner.setRom(new OP_SP_HL_03());
        gameBoyRunner.setSerialDevice(this);
        gameBoyRunner.start();
        assertTrue(this.isTestPassed(gameBoyRunner));
    }

    @Test
    public void test_06_LD_R_R() throws IOException {
        GameBoyRunner gameBoyRunner = new GameBoyRunner();
        gameBoyRunner.setRom(new LD_R_R_06());
        gameBoyRunner.setSerialDevice(this);
        gameBoyRunner.start();
        assertTrue(this.isTestPassed(gameBoyRunner));
    }



}
