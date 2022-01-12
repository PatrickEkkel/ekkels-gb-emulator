import core.cpu.flags.utils.FlagUtils;
import core.cpu.flags.utils.FlagsHelper;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.cpu.registers.utils.RegisterHelper;
import core.mmu.Computable;
import core.mmu.MemoryAddress;
import core.mmu.MemoryValue;
import ekkel.gameboy.Gameboy;
import ekkel.gameboy.TestBoy;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;


 public class OpcodeTests extends OpcodeTestBase {

    @Test
    public void testDI() throws NotImplementedException, IllegalAccessException {
        Gameboy gameboy = this.createTestContext(0x0,0x100,"DI");
        gameboy.powerOn();

        Computable value =  gameboy.getMMU().read(MemoryAddress.fromValue(0xFFFF));
        assert  value.getValue() == 0x0000;
    }
    @Test
    public void testJPa16() {
        Gameboy gameboy = this.createTestContext(0x0,0x100,"JP 0x1000");
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.PC).getValue() == 0x1000;
    }

    @Test
    public void testLD_SP_d16() {
        Gameboy gameboy = this.createTestContext(0x0,0x100,"LD SP 0x1010");
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister((Registers.SP)).getValue() == 0x1010;
    }
    @Test
    public void testLD_HL_d16() {
        Gameboy gameboy = this.createTestContext(0x0,0x100,"LD HL 0x1010");
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.HL).getValue() == 0x1010;
    }

    @Test
    public void test_LD_a16_A() throws NotImplementedException, IllegalAccessException {
        Gameboy gameboy = this.createTestContext(0x0,0x100,"LD 0xD600 A");
        gameboy.getCPU().readRegister(Registers.A).setValue(0x10);
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.A).getValue() == gameboy.getMMU().read(MemoryAddress.fromValue(0xD600)).getValue();
    }
    @Test
    public void test_LD_A_d8() {
        Gameboy gameboy = this.createTestContext(0x0,0x100,"LD A 0x10");
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.A).getValue() == 0x10;
    }
    @Test
    public void test_CALL_a16() {
        Gameboy gameboy = this.createTestContext(0x0,0x100,"CALL 0x1200");
        gameboy.getCPU().readRegister(Registers.SP).setValue(0xDFFF);
        gameboy.powerOn();

        assert gameboy.getCPU().readRegister(Registers.SP).getValue() == 0xDFFD;
        assert gameboy.getCPU().readRegister(Registers.PC).getValue() == 0x1200;
    }
    @Test
    public void test_LD_A_L() {
        Gameboy gameboy = this.createTestContext(0x0,0x100,"LD A L");
        gameboy.getCPU().readRegister(Registers.A).setValue(0x10);
        gameboy.getCPU().readRegister(Registers.L).setValue(0x66);
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.A).getValue() == 0x66;

    }
    @Test
    public void test_LD_A_H() {
        Gameboy gameboy = this.createTestContext(0x0,0x100,"LD A H");
        gameboy.getCPU().readRegister(Registers.A).setValue(0x10);
        gameboy.getCPU().readRegister(Registers.H).setValue(0x66);
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.A).getValue() == 0x66;
    }
     @Test
     public void test_LD_A_B() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD A B");
         gameboy.getCPU().readRegister(Registers.A).setValue(0x10);
         gameboy.getCPU().readRegister(Registers.B).setValue(0x66);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.A).getValue() == 0x66;
     }
     @Test
     public void test_LD_A_C() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD A C");
         gameboy.getCPU().readRegister(Registers.A).setValue(0x10);
         gameboy.getCPU().readRegister(Registers.C).setValue(0x66);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.A).getValue() == 0x66;
     }
     @Test
     public void test_LD_A_D() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD A D");
         gameboy.getCPU().readRegister(Registers.A).setValue(0x10);
         gameboy.getCPU().readRegister(Registers.D).setValue(0x66);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.A).getValue() == 0x66;
     }

     @Test
     public void test_LD_A_E() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD A E");
         gameboy.getCPU().readRegister(Registers.A).setValue(0x10);
         gameboy.getCPU().readRegister(Registers.E).setValue(0x66);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.A).getValue() == 0x66;
     }
     @Test
     public void test_LD_A_A() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD A A");
         gameboy.getCPU().readRegister(Registers.A).setValue(0x66);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.A).getValue() == 0x66;
     }
     @Test
     public void test_LD_B_A() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD B A");
         gameboy.getCPU().readRegister(Registers.B).setValue(0x10);
         gameboy.getCPU().readRegister(Registers.A).setValue(0x66);

         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.B).getValue() == 0x66;
     }
     @Test
     public void test_LD_B_B() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD B B");
         gameboy.getCPU().readRegister(Registers.B).setValue(0x10);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.B).getValue() == 0x10;
     }
     @Test
     public void test_LD_B_C() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD B C");
         gameboy.getCPU().readRegister(Registers.B).setValue(0x10);
         gameboy.getCPU().readRegister(Registers.C).setValue(0x66);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.B).getValue() == 0x66;
     }
     @Test
     public void test_LD_B_D() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD B D");
         gameboy.getCPU().readRegister(Registers.B).setValue(0x10);
         gameboy.getCPU().readRegister(Registers.D).setValue(0x66);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.B).getValue() == 0x66;
     }
     @Test
     public void test_LD_B_E() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD B E");
         gameboy.getCPU().readRegister(Registers.B).setValue(0x10);
         gameboy.getCPU().readRegister(Registers.E).setValue(0x66);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.B).getValue() == 0x66;
     }
     @Test
     public void test_LD_B_H() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD B H");
         gameboy.getCPU().readRegister(Registers.B).setValue(0x10);
         gameboy.getCPU().readRegister(Registers.H).setValue(0x66);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.B).getValue() == 0x66;
     }
     @Test
     public void test_LD_B_L() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD B L");
         gameboy.getCPU().readRegister(Registers.B).setValue(0x10);
         gameboy.getCPU().readRegister(Registers.L).setValue(0x66);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.B).getValue() == 0x66;
     }
     @Test
     public void test_LD_C_A() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD C A");
         gameboy.getCPU().readRegister(Registers.C).setValue(0x10);
         gameboy.getCPU().readRegister(Registers.A).setValue(0x66);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.C).getValue() == 0x66;
     }
     @Test
     public void test_LD_C_B() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD C B");
         gameboy.getCPU().readRegister(Registers.C).setValue(0x10);
         gameboy.getCPU().readRegister(Registers.B).setValue(0x66);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.C).getValue() == 0x66;
     }
     @Test
     public void test_LD_C_D() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD C D");
         gameboy.getCPU().readRegister(Registers.C).setValue(0x10);
         gameboy.getCPU().readRegister(Registers.D).setValue(0x66);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.C).getValue() == 0x66;
     }
     @Test
     public void test_LD_C_E() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD C E");
         gameboy.getCPU().readRegister(Registers.C).setValue(0x10);
         gameboy.getCPU().readRegister(Registers.E).setValue(0x66);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.C).getValue() == 0x66;
     }
     @Test
     public void test_LD_D_D() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD D D");
         gameboy.getCPU().readRegister(Registers.D).setValue(0x10);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.D).getValue() == 0x10;

     }

     @Test
     public void test_LD_D_A() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD D A");
         gameboy.getCPU().readRegister(Registers.D).setValue(0x10);
         gameboy.getCPU().readRegister(Registers.A).setValue(0x66);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.D).getValue() == 0x66;
     }

     @Test
     public void test_LD_D_B() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD D B");
         gameboy.getCPU().readRegister(Registers.D).setValue(0x10);
         gameboy.getCPU().readRegister(Registers.B).setValue(0x66);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.D).getValue() == 0x66;
     }

     @Test
     public void test_LD_D_C() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD D C");
         gameboy.getCPU().readRegister(Registers.D).setValue(0x10);
         gameboy.getCPU().readRegister(Registers.C).setValue(0x66);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.D).getValue() == 0x66;
     }
     @Test
     public void test_LD_D_E() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD D E");
         gameboy.getCPU().readRegister(Registers.D).setValue(0x10);
         gameboy.getCPU().readRegister(Registers.E).setValue(0x66);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.D).getValue() == 0x66;
     }
     @Test
     public void test_LD_D_H() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD D H");
         gameboy.getCPU().readRegister(Registers.D).setValue(0x10);
         gameboy.getCPU().readRegister(Registers.H).setValue(0x66);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.D).getValue() == 0x66;
     }

     @Test
     public void test_LD_H_H() {
         Gameboy gameboy = this.createTestContext(0x0,0x100,"LD H H");
         gameboy.getCPU().readRegister(Registers.H).setValue(0x10);
         gameboy.powerOn();
         assert gameboy.getCPU().readRegister(Registers.H).getValue() == 0x10;
     }



    @Test
    public void test_JR_r8() {
        Gameboy gameboy = this.createTestContext(0x0,0x5,"JR s5");
      //  gameboy.getCPU().reg.get(Registers.PC).setValue(0x110);
        gameboy.powerOn();
        // JR s8 is 2 bytes long, + 5 means the relative jump should be at 0x7
        assert gameboy.getCPU().readRegister(Registers.PC).getValue() == 0x7;

    }
    @Test
    public void test_PUSH_HL() throws NotImplementedException, IllegalAccessException {

        Gameboy gameboy = this.createTestContext(0x0,0x5,"PUSH HL");
        gameboy.getCPU().readRegister(Registers.SP).setValue(0xDFFF);
        gameboy.getCPU().readRegister(Registers.HL).setValue(0xF00F);
        gameboy.powerOn();
        assert gameboy.getMMU().read(MemoryAddress.fromValue(0xDFFF)).getValue() == 0xF0;
        assert gameboy.getMMU().read(MemoryAddress.fromValue(0xDFFE)).getValue() == 0x0F;

    }
    @Test
    public void test_PUSH_DE() throws NotImplementedException, IllegalAccessException {

        Gameboy gameboy = this.createTestContext(0x0,0x5,"PUSH DE");
        gameboy.getCPU().readRegister(Registers.SP).setValue(0xDFFF);
        gameboy.getCPU().readRegister(Registers.DE).setValue(0xF00F);
        gameboy.powerOn();
        assert gameboy.getMMU().read(MemoryAddress.fromValue(0xDFFF)).getValue() == 0xF0;
        assert gameboy.getMMU().read(MemoryAddress.fromValue(0xDFFE)).getValue() == 0x0F;

    }
    @Test
    public void test_PUSH_BC() throws NotImplementedException, IllegalAccessException {

        Gameboy gameboy = this.createTestContext(0x0,0x5,"PUSH BC");
        gameboy.getCPU().readRegister(Registers.SP).setValue(0xDFFF);
        gameboy.getCPU().readRegister(Registers.BC).setValue(0xF00F);
        gameboy.powerOn();
        assert gameboy.getMMU().read(MemoryAddress.fromValue(0xDFFF)).getValue() == 0xF0;
        assert gameboy.getMMU().read(MemoryAddress.fromValue(0xDFFE)).getValue() == 0x0F;

    }
    @Test
    public void test_PUSH_AF() throws NotImplementedException, IllegalAccessException {

        Gameboy gameboy = this.createTestContext(0x0,0x5,"PUSH AF");
        gameboy.getCPU().readRegister(Registers.SP).setValue(0xDFFF);
        gameboy.getCPU().readRegister(Registers.AF).setValue(0xF00F);
        gameboy.powerOn();
        assert gameboy.getMMU().read(MemoryAddress.fromValue(0xDFFF)).getValue() == 0xF0;
        assert gameboy.getMMU().read(MemoryAddress.fromValue(0xDFFE)).getValue() == 0x0F;


    }

    @Test
    public void test_POP_HL() {

        Gameboy gameboy = this.createTestContext(0x0,0x5,"PUSH HL","LD HL 0x0000","POP HL");
        gameboy.getCPU().readRegister(Registers.SP).setValue(0xDFFF);
        gameboy.getCPU().readRegister(Registers.HL).setValue(0xF00F);
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.HL).getValue() == 0xF00F;
    }
    @Test
    public void test_POP_DE()  {

        Gameboy gameboy = this.createTestContext(0x0,0x5,"PUSH DE","LD DE 0x0000","POP DE");
        gameboy.getCPU().readRegister(Registers.SP).setValue(0xDFFF);
        gameboy.getCPU().readRegister(Registers.DE).setValue(0xF00F);
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.DE).getValue() == 0xF00F;
    }
    @Test
    public void test_POP_BC() {

        Gameboy gameboy = this.createTestContext(0x0,0x5,"PUSH BC","LD BC 0x0000","POP BC");
        gameboy.getCPU().readRegister(Registers.SP).setValue(0xDFFF);
        gameboy.getCPU().readRegister(Registers.BC).setValue(0xF00F);
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.BC).getValue() == 0xF00F;
    }
    @Test
    public void test_INC_HL() {
        Gameboy gameboy = this.createTestContext(0x0,0x5,"INC HL");
        gameboy.getCPU().readRegister(Registers.HL).setValue(0x1010);
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.HL).getValue() == 0x1011;
    }

    @Test
    public void test_INC_BC() {
        Gameboy gameboy = this.createTestContext(0x0,0x5,"INC BC");
        gameboy.getCPU().readRegister(Registers.BC).setValue(0x1010);
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.BC).getValue() == 0x1011;
    }

    @Test
    public void test_INC_DE() {
        Gameboy gameboy = this.createTestContext(0x0,0x5,"INC DE");
        gameboy.getCPU().readRegister(Registers.DE).setValue(0x1010);
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.DE).getValue() == 0x1011;
    }
    @Test
    public void test_INC_SP() {
        Gameboy gameboy = this.createTestContext(0x0,0x5,"INC SP");
        gameboy.getCPU().readRegister(Registers.SP).setValue(0x1010);
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.SP).getValue() == 0x1011;
    }
    @Test
    public void test_LDI_A_HL() throws NotImplementedException {
        Gameboy gameboy = this.createTestContext(0x0,0x5,"LDI A HL");
        gameboy.getMMU().write(MemoryAddress.fromValue(0xD001), MemoryValue.fromValue(0xF00F));
        gameboy.getCPU().readRegister(Registers.HL).setValue(0xD001);
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.HL).getValue() == 0xD002;
        assert gameboy.getCPU().readRegister(Registers.A).getValue() == 0xF0;
    }

    @Test
    public void test_OR_C() {
        Gameboy gameboy = this.createTestContext(0x0,0x5,"OR C");
        gameboy.getCPU().writeRegister(Registers.A,MemoryValue.fromValue(0xFB));
        gameboy.getCPU().writeRegister(Registers.C,MemoryValue.fromValue(0x1F));
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.A).getValue() == 0xFF;
        //assert gameboy.getCPU().readRegister(Registers.F).getValue() == 0x00;
    }
    @Test
    public void test_JR_Z() {
        String [] program = new String [] {"NOP","NOP","NOP","NOP","NOP","NOP","JRZ s-5"};
        TestBoy gameboy = this.createTestContext(0x00,0x50,program);
        // limit the amount of clockcycles to 36, to prevent the testprogram from looping endlessly
        gameboy.setLimitClockticks(36);
        // set zero flag
        gameboy.getCPU().readRegister(Registers.F).setValue(0x80);
        gameboy.powerOn();
        // current position after execution of JRZ s -5 should be 2, also jump should be triggered because zero flag isset
        assert gameboy.getCPU().readRegister(Registers.PC).getValue() == 3;
    }
    @Test
    public void test_CP_d8_HC() {
        TestBoy gameboy = this.createTestContext(0x00,0x50,"CP 0x0A");
       // gameboy.getCPU().readRegister(Registers.A).setValue(0x88);
        gameboy.getCPU().readRegister(Registers.A).setValue(0x63);
        gameboy.powerOn();

        int flags = gameboy.getCPU().readRegister(Registers.F).getValue();
        assert flags == 0x60;

    }

    @Test
    public void test_CP_d8_A0() {
        TestBoy gameboy = this.createTestContext(0x00,0x50,"CP 0x0A","JRZ s2","LD A 0x10","LD A 0x20");
        gameboy.getCPU().readRegister(Registers.AF).setValue(0x0AC0);
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.A).getValue() == 0x20;
    }

    @Test
    public void test_CP_d8() {

        TestBoy gameboy = this.createTestContext(0x00,0x50,"CP 0x88");
        gameboy.getCPU().readRegister(Registers.A).setValue(0x88);
        gameboy.powerOn();


    }
    @Test
    public void test_CP_d8_c_hc() {
        TestBoy gameboy = this.createTestContext(0x00,0x50,"CP 0x90");
        gameboy.getCPU().readRegister(Registers.A).setValue(0x90);
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.F).getValue() == 0xC0;
    }


    @Test
    public void test_DEC_B() {
        TestBoy gameboy = this.createTestContext(0x00,0x50,"DEC B");
        gameboy.getCPU().readRegister(Registers.B).setValue(0x20);
        gameboy.powerOn();

        assert gameboy.getCPU().readRegister(Registers.B).getValue() == 0x1F;
    }
    @Test
    public void LD_B_d8() {
        TestBoy gameboy = this.createTestContext(0x00,0x50,"LD B 0x20");
        gameboy.getCPU().readRegister(Registers.B).setValue(0x00);
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.B).getValue() == 0x20;
    }

    @Test
    public void AND_d8() {
        TestBoy gameboy = this.createTestContext(0x00,0x50,"AND 0x80");
        gameboy.getCPU().readRegister(Registers.A).setValue(0x81);
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.A).getValue() == 0x80;
    }

    public void CALL_NZ_d16() {
        TestBoy gameboy = this.createTestContext(0x00,0x200,"CALLNZ 0x0100");
        gameboy.setLimitClockticks(24);
        gameboy.powerOn();
        assert  gameboy.getCPU().readRegister(Registers.PC).getValue() == 0x100;
    }

    @Test
    public void SRL_B() {
        TestBoy gameboy = this.createTestContext(0x00,0x50,"CB","SRL B");
        gameboy.getCPU().readRegister(Registers.B).setValue(0xFF);
        gameboy.powerOn();

        assert gameboy.getCPU().readRegister(Registers.B).getValue() == 0x7F;
        assert gameboy.getCPU().readRegister(Registers.F).getValue() == gameboy.getCPU().getCarryFlag().getValue();
    }
    @Test
    public void RR_C() {
        TestBoy gameboy = this.createTestContext(0x00,0x50,"CB","RR C");
        // set the carryflag
        gameboy.getCPU().readRegister(Registers.F).set(gameboy.getCPU().getCarryFlag());
        // set the value to a bit that will be carried
        gameboy.getCPU().readRegister(Registers.C).setValue(0x03);
        gameboy.powerOn();
        // we expect the carry flag to be set
        gameboy.getCPU().readRegister(Registers.F).and(gameboy.getCPU().getCarryFlag());
        assert gameboy.getCPU().readRegister(Registers.C).getValue() == 0x81;
        assert gameboy.getCPU().readRegister(Registers.F)
                .and(gameboy.getCPU().getCarryFlag()).equals(gameboy.getCPU().getCarryFlag());
    }

    @Test
    public void test_RLCA() {
        TestBoy gameboy = this.createTestContext(0x00,0x50,"RLCA");
        gameboy.getCPU().readRegister(Registers.AF).setValue(0x7E20);
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.A).getValue() == 0xFC;
    }
    @Test
    public void test_SWAP_A() {
        TestBoy gameboy = this.createTestContext(0x00,0x50,"CB","SWAP A");
        gameboy.getCPU().readRegister(Registers.A).setValue(0xAF);
        gameboy.powerOn();
        assert gameboy.getCPU().readRegister(Registers.A).getValue() == 0xFA;
    }
    @Test
    public void test_ADD_HL_SP_base_1() {
        TestBoy gameboy = this.createTestContext(0x00, 0x50,"ADD HL SP");
        gameboy.getCPU().readRegister(Registers.HL).setValue(0xFF);
        gameboy.getCPU().readRegister(Registers.SP).setValue(0x01);
        gameboy.powerOn();

        assert gameboy.getCPU().readRegister(Registers.HL).getValue() == 0x100;
    }


     @Test
     public void test_ADD_HL_SP_base_2() {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"ADD HL SP");
         gameboy.getCPU().readRegister(Registers.HL).setValue(0x1);
         gameboy.getCPU().readRegister(Registers.SP).setValue(0x7FFF);
         gameboy.getCPU().readRegister(Registers.AF).setValue(0x1200);
         gameboy.powerOn();

         assert gameboy.getCPU().readRegister(Registers.HL).getValue() == 0x8000;
         assert gameboy.getCPU().readRegister(Registers.AF).getValue() == 0x1220;
     }

     @Test
     public void test_ADD_HL_SP_base_3() {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"ADD HL SP");
         gameboy.getCPU().readRegister(Registers.HL).setValue(0x1);
         gameboy.getCPU().readRegister(Registers.SP).setValue(0xFF);
         gameboy.getCPU().readRegister(Registers.AF).setValue(0x12F0);
         gameboy.powerOn();

         assert gameboy.getCPU().readRegister(Registers.HL).getValue() == 0x100;
         assert gameboy.getCPU().readRegister(Registers.AF).getValue() == 0x1280;
     }

     @Test
     public void test_ADD_HL_SP_base_4() {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"ADD HL SP");
         gameboy.getCPU().readRegister(Registers.HL).setValue(0x10);
         gameboy.getCPU().readRegister(Registers.SP).setValue(0x7F);
         gameboy.getCPU().readRegister(Registers.AF).setValue(0x12F0);
         gameboy.powerOn();

         assert gameboy.getCPU().readRegister(Registers.HL).getValue() == 0x8F;
         assert gameboy.getCPU().readRegister(Registers.AF).getValue() == 0x1280;
     }

     @Test
     public void test_ADD_SP_r8_base_1() {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"ADD SP s1");

         gameboy.getCPU().readRegister(Registers.SP).setValue(0x8000);
         gameboy.getCPU().readRegister(Registers.AF).setValue(0x1200);

         gameboy.powerOn();
         assertEquals(0x8001,gameboy.getCPU().readRegister(Registers.SP).getValue());
         testFlags(gameboy,gameboy.getCPU().readRegister(Registers.F).getValue(),0x00);
     }

     @Test
     public void test_ADD_SP_r8_base_2() {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"ADD SP s-1");
         RegisterHelper registerHelper = gameboy.getRegisterHelper();

         gameboy.getCPU().readRegister(Registers.SP).setValue(0x80);
         gameboy.getCPU().readRegister(Registers.AF).setValue(0x1200);

         gameboy.powerOn();
         assertEquals(0x7F,registerHelper.toInt(Registers.SP));
         testFlags(gameboy,gameboy.getCPU().readRegister(Registers.F).getValue(),0x10);
     }
     @Test
     public void test_SBC_A_base_1() {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"SBC A 0x05");
         RegisterHelper registerHelper = gameboy.getRegisterHelper();
         FlagsHelper flagsHelper = gameboy.getFlagsHelper();
         FlagUtils.setFlag(registerHelper.getRegister(Registers.F),flagsHelper.getC());
         registerHelper.setRegister(Registers.A,0x16);
         gameboy.powerOn();
         assertTrue(registerHelper.isEqual(Registers.A,0x10));
     }

     @Test
     /*
       Test if XOR behaves correctly when feeding it signed numbers
      */
     public void test_XOR_L_A_base_1() {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"XOR L","LD L A");
         RegisterHelper registerHelper = gameboy.getRegisterHelper();
         registerHelper.setRegister(Registers.A,0xFE);
         registerHelper.setRegister(Registers.L, -1);
         gameboy.powerOn();
         assertTrue(registerHelper.isEqual(Registers.L,0x1));
     }

     @Test
     public void test_LD_HL_d8_base_1() throws NotImplementedException, IllegalAccessException {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"LD (HL) 0x10");
         RegisterHelper registerHelper = gameboy.getRegisterHelper();
         registerHelper.setRegister(Registers.HL,0xDEF4);
         gameboy.powerOn();
         MemoryValue memoryValue = gameboy.getMMU().read(MemoryAddress.fromValue(0xDEF4));
         assertEquals(0x10,memoryValue.getValue());
     }

     @Test
     public void test_CP_d8_base_1() {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"CP 0x00");
         RegisterHelper registerHelper = gameboy.getRegisterHelper();
         registerHelper.setRegister(Registers.AF,0x10);
         gameboy.powerOn();
         testFlags(gameboy,gameboy.getCPU().readRegister(Registers.F).getValue(),0xC0);
     }
     @Test
     public void test_LD_B_d8() {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"LD B 0x10");
         RegisterHelper registerHelper = gameboy.getRegisterHelper();
         gameboy.powerOn();
         assertTrue(registerHelper.isEqual(Registers.B,0x10));
     }

    @Test
     public void test_ADD_A_d8_base_1() {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"ADD A 0x00");
         RegisterHelper registerHelper = gameboy.getRegisterHelper();
         registerHelper.setRegister(Registers.AF,0xFFF0);
         gameboy.powerOn();
         assertTrue(registerHelper.isEqual(Registers.A,0xFF));
         testFlags(gameboy,gameboy.getCPU().readRegister(Registers.F).getValue(),0x00);

     }
     @Test
     public void test_ADD_A_d8_base_2() {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"ADD A 0x1F");
         RegisterHelper registerHelper = gameboy.getRegisterHelper();
         registerHelper.setRegister(Registers.AF,0xF0F0);
         gameboy.powerOn();
         assertTrue(registerHelper.isEqual(Registers.A,0xF));
         testFlags(gameboy,gameboy.getCPU().readRegister(Registers.F).getValue(),0x10);
     }
     @Test
     public void test_ADC_A_d8_base_1() {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"ADC A 0x10");
         RegisterHelper registerHelper = gameboy.getRegisterHelper();
         FlagsHelper flagsHelper = gameboy.getFlagsHelper();
         flagsHelper.setC();
         registerHelper.setRegister(Registers.A,0x16);

         gameboy.powerOn();
         assertTrue(registerHelper.isEqual(Registers.A,0x27));
        // testFlags(gameboy,gameboy.getCPU().readRegister(Registers.F).getValue(),0x10);

     }
     @Test
     public void test_ADC_A_d8_base_2() {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"ADC A 0x00");
         RegisterHelper registerHelper = gameboy.getRegisterHelper();
         FlagsHelper flagsHelper = gameboy.getFlagsHelper();
         flagsHelper.setC();
         registerHelper.setRegister(Registers.A,0xF);
         gameboy.powerOn();
         assertTrue(registerHelper.isEqual(Registers.A,0x10));
     }


     @Test
     public void test_ADC_A_d8_base_3() {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"ADC A 0x00");
         RegisterHelper registerHelper = gameboy.getRegisterHelper();
         FlagsHelper flagsHelper = gameboy.getFlagsHelper();
         flagsHelper.setC();
         registerHelper.setRegister(Registers.A,0xF);
         gameboy.powerOn();
         assertTrue(registerHelper.isEqual(Registers.A,0x10));
         testFlags(gameboy,gameboy.getCPU().readRegister(Registers.F).getValue(),0x20);
     }
     @Test
     public void test_ADC_A_d8_base_4() {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"ADC A 0xF0");
         RegisterHelper registerHelper = gameboy.getRegisterHelper();
         FlagsHelper flagsHelper = gameboy.getFlagsHelper();
         flagsHelper.setC();
         registerHelper.setRegister(Registers.A,0x1F);
         //  registerHelper.setRegister(Registers.F,0x00);
         gameboy.powerOn();
         assertTrue(registerHelper.isEqual(Registers.A,0x10));
         testFlags(gameboy,gameboy.getCPU().readRegister(Registers.F).getValue(),0x30);
     }
     @Test
     public void test_ADC_A_d8_base_5() {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"ADC A 0x0F");
         RegisterHelper registerHelper = gameboy.getRegisterHelper();
         FlagsHelper flagsHelper = gameboy.getFlagsHelper();
         flagsHelper.setC();
         registerHelper.setRegister(Registers.A,0xF);
         gameboy.powerOn();
         assertTrue(registerHelper.isEqual(Registers.A,0x1F));
         testFlags(gameboy,gameboy.getCPU().readRegister(Registers.F).getValue(),0x20);

     }

     @Test
     public void test_ADC_A_d8_base_6() {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"ADC A 0x00");
         RegisterHelper registerHelper = gameboy.getRegisterHelper();
         FlagsHelper flagsHelper = gameboy.getFlagsHelper();
         flagsHelper.setC();
         registerHelper.setRegister(Registers.A,0xFF);
         registerHelper.setRegister(Registers.F,0xB0);

         gameboy.powerOn();
         assertTrue(registerHelper.isEqual(Registers.A,0x0));
         testFlags(gameboy,gameboy.getCPU().readRegister(Registers.F).getValue(),0xB0);

     }
     @Test
     public void test_SBC_A_d8_base_1() {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"SBC A 0x10");
         RegisterHelper registerHelper = gameboy.getRegisterHelper();
         FlagsHelper flagsHelper = gameboy.getFlagsHelper();
         flagsHelper.setC();
         registerHelper.setRegister(Registers.A,0x0F);
         registerHelper.setRegister(Registers.F,0x10);

         gameboy.powerOn();
         assertTrue(registerHelper.isEqual(Registers.A,0xFE));
     }
     @Test
     public void test_SBC_A_d8_base_2() {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"SBC A 0x00");
         RegisterHelper registerHelper = gameboy.getRegisterHelper();
         FlagsHelper flagsHelper = gameboy.getFlagsHelper();
         flagsHelper.setC();
         registerHelper.setRegister(Registers.A,0x00);
        // registerHelper.setRegister(Registers.F,0x10);

         gameboy.powerOn();
         assertTrue(registerHelper.isEqual(Registers.A,0xFF));
     }

     @Test
     public void test_SBC_A_d8_base_3() {
         TestBoy gameboy = this.createTestContext(0x00, 0x50,"SBC A 0x01");
         RegisterHelper registerHelper = gameboy.getRegisterHelper();
         FlagsHelper flagsHelper = gameboy.getFlagsHelper();
         flagsHelper.setC();
         registerHelper.setRegister(Registers.A,0x00);
         gameboy.powerOn();
         assertTrue(registerHelper.isEqual(Registers.A,0xFE));
         testFlags(gameboy,gameboy.getCPU().readRegister(Registers.F).getValue(),0x70);
     }

}
