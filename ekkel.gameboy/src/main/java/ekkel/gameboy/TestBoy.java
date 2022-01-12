package ekkel.gameboy;

import core.cpu.flags.utils.FlagsHelper;
import core.cpu.opcodes.exceptions.DivergedCPUStateException;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.opcodes.exceptions.UnknownOpcodeException;
import core.cpu.registers.Registers;
import core.cpu.registers.utils.RegisterHelper;

public class TestBoy extends Gameboy {
    private int stopAt;
    private int limitClockticks;
    public TestBoy(int PC,int stopAt) {
        super(false);
        this.cpu.setPC(PC);
        this.stopAt = stopAt;
        this.limitClockticks = -1;

    }

    public void setLimitClockticks(int limitClockticks) {
        this.limitClockticks = limitClockticks;
    }

     public RegisterHelper getRegisterHelper() {
        return new RegisterHelper(this.getCPU());
     }

     public FlagsHelper getFlagsHelper() {
        return new FlagsHelper(this.getCPU(),this.cpu.readRegister(Registers.F));
     }

    @Override
    public void powerOn() {
        int PC =  this.cpu.readRegister(Registers.PC).getValue();
        int ticks = 0;
        do {
            try {
               ticks += this.cpu.tick(ticks);
               if(this.limitClockticks > 0 && ticks >= this.limitClockticks) {
                   break;
               }
               PC = this.cpu.readRegister(Registers.PC).getValue();
            } catch (NotImplementedException | IllegalAccessException | UnknownOpcodeException | DivergedCPUStateException e) {
                e.printStackTrace();
                return;
            }
        } while (PC <= this.stopAt);
    }
}
