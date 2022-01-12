package ekkel.gameboy.ppu;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.MMU;
import core.mmu.MemoryAddress;
import core.mmu.MemoryValue;
import ekkel.gameboy.cpu.IOMap;
import ekkel.gameboy.screen.Screen;

import java.util.Collections;
import java.util.List;
import java.util.Stack;

public class FIFO {

    private Stack<Integer> pixels;
    private MMU mmuImpl;
    private Screen screen;


    public FIFO(MMU mmuImpl) {
        this.pixels = new Stack<>();
        this.mmuImpl = mmuImpl;
    }

    public void setScreen(Screen screen) {
        this.screen = screen;
    }


    public void pushBlock(List<Integer> pixels) {
        Collections.reverse(pixels);
        this.pixels.addAll(pixels);
    }

    public void clear() {
        this.pixels = new Stack<>();
    }

    public void shift() throws NotImplementedException, IllegalAccessException {
        Integer pixel = this.pixels.pop();
        MemoryValue LY = this.mmuImpl.read(MemoryAddress.fromValue(IOMap.LY));
        this.screen.putPixel(LY.getValue(), pixel);
    }

    public boolean isFilled() {
        return this.pixels.size() > 8;
    }

    public boolean isReady() {
        return this.pixels.size() <= 8;

    }
}
