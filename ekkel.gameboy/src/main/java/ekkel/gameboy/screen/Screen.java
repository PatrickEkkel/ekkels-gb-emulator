package ekkel.gameboy.screen;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.Computable;
import core.mmu.MMUComponent;
import core.mmu.MemoryAddress;
import core.mmu.MemoryValue;
import core.mmu.memorymap.MemoryMapEntry;
import ekkel.gameboy.cpu.IOMap;
import gui.Display;
import gui.GameBoyDMGPalette;

import java.util.ArrayList;
import java.util.List;

/**
 * Represents the Gameboy LCD Screen, its purpose is to serve as a interface between the gameboy system and the GUI
 * Additonally it holds the LCDC Register,
 */
public class Screen extends MMUComponent {

    public final int WIDTH = 161;
    public final int HEIGHT = 155;
    private int scale = 4;
    private Display display;
    private int currentX;

    // LCD_DISPLAY_ENABLE BIT in LCDC
    private final int LCD_DISPLAY_ENABLE = 7;

    private MemoryValue lcdc;

    public Screen() {
        this.lcdc = MemoryValue.empty();
        this.display = new Display(WIDTH,HEIGHT, scale);
        GameBoyDMGPalette gameBoyDMGPalette = new GameBoyDMGPalette();
        this.display.setPalette(gameBoyDMGPalette);
        this.currentX = 0;
        init();
    }

    public void init() {
         for(int y=0;y<this.HEIGHT;y++) {
            for(int x=0;x<this.WIDTH;x++) {
                display.putPixel(x,y,GameBoyDMGPalette.WHITE);
            }
        }
         refresh();
    }


    public Display getDisplay() {
        return this.display;
    }
    @Override
    public void write(MemoryAddress memoryAddress, MemoryValue value) throws NotImplementedException {
        this.lcdc = value;
    }

    private boolean isDisplayEnabled() {
        // disable display hardcoded.. and focus on CPU implemtation first
        return this.lcdc.getBit(LCD_DISPLAY_ENABLE);
    }

    @Override
    public MemoryValue read(MemoryAddress memoryAddress) throws NotImplementedException, IllegalAccessException {
        return lcdc;
    }

    @Override
    public boolean IsAddressed(MemoryAddress memoryAddress) throws NotImplementedException {
        return memoryAddress.getValue() == IOMap.LCDC;
    }

    @Override
    public List<MemoryMapEntry> getComponentIds() {
        List<MemoryMapEntry> memoryMapEntries = new ArrayList<>();
        MemoryMapEntry memoryMapEntry = new MemoryMapEntry();
        memoryMapEntry.addRegister(IOMap.LCDC,"LCDC");
        memoryMapEntries.add(memoryMapEntry);
        return memoryMapEntries;
    }

    public void newScanline() {
        this.currentX = 0;
    }

    public void refresh() {
        if(isDisplayEnabled()) {
            this.display.refresh();
        }
    }

    public void putPixel(int y, int color) {
        if(this.isDisplayEnabled()) {
            this.currentX += 1;
            this.display.putPixel(this.currentX, y, color);
        }
    }
}
