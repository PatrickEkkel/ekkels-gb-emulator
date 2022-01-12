package ekkel.gameboy.ppu;

import core.cpu.opcodes.exceptions.NotImplementedException;

public class DummyPPU  extends PPU {

    @Override
    public void tick(long cycles) throws NotImplementedException, IllegalAccessException {
        this.cycleCount += cycles / 4;
      //  this.incLY();
        this.drawPointer.setLY(0x90);
        if (this.cycleCount >= 114) {
            this.cycleCount = this.cycleCount - 114;
        }
    }
}
