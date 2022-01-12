package ekkel.gameboy.ppu;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.MMU;
import core.mmu.MMUComponent;
import core.mmu.MemoryAddress;
import core.mmu.MemoryValue;
import core.mmu.memorymap.MemoryMap;
import core.mmu.memorymap.MemoryMapEntry;
import ekkel.gameboy.cpu.IOMap;
import ekkel.gameboy.ppu.vram.VRAM;
import ekkel.gameboy.screen.Screen;

import java.util.ArrayList;
import java.util.List;

public class PPU extends MMUComponent implements MMU {

    protected int cycleCount = 0;
    private PpuState state;
    private List<MMUComponent> ppuBus;
    private Fetcher fetcher;
    private Screen screen;
    private FIFO fifo;
    protected DrawPointer drawPointer;

    private static final int TILERAM_START_0 = 0x8800;
    private static final int TILERAM_END_0 = 0x97FF;

   // private static final int TILERAM_START_1 = 0x8800;
   //  private static final int TILERAM_END_1 = 0x8FFF;

    private static final int TILERAM_START_1 = 0x8000;
    private static final int TILERAM_END_1 = 0x97FF;

    private static final int BACKGROUND_MAP_START_0 = 0x9800;
    private static final int BACKGROUND_MAP_END_0 = 0x9BFF;
    private static final int BACKGROUND_MAP_START_1 = 0x9C00;
    private static final int BACKGROUND_MAP_END_1 = 0x9FFF;

    private int tc;
    private int tileIndex;

    private MemoryMap memoryMap;

    //  BG_TILE_MAP_DISPLAY_SELECT BIT in LCDC
    private int BG_TILE_MAP_DISPLAY_SELECT = 3;
    // WINDOW_TILE_MAP_DISPLAY_SELECT in LCDC
    private int WINDOW_TILE_MAP_DISPLAY_SELECT = 6;
    // BG_WINDOWS_TILE_DATA_SELECT in LCDC
    private int BG_WINDOWS_TILE_DATA_SELECT = 4;

    public PPU() {
        this.memoryMap = new MemoryMap();
        // 0x90 appears to by a sane starting value for 0xFF44
        this.drawPointer = new DrawPointer(0x00,0x90);
        this.ppuBus = new ArrayList<>();
        this.connect(new VRAM());
        // fetcher and fifo pipeline should only have access to the VRAM portion, PPU controls all access to VRAM
        this.fetcher = new Fetcher(this);
        this.fetcher.setOffset(BACKGROUND_MAP_START_0);
        this.fetcher.setTilemapRam(TILERAM_START_1);
        this.fifo = new FIFO(this);

        //  tilecounter
        this.tc = 0;
        // tileindex
        this.tileIndex = 0;
        this.state = PpuState.OAM_SEARCH;
    }

    private void handleBgTileMapSwitch(MemoryValue value) {
        if(value.getBit(BG_TILE_MAP_DISPLAY_SELECT)) {
            fetcher.setOffset(BACKGROUND_MAP_START_1);
        }
        else {
            fetcher.setOffset(BACKGROUND_MAP_START_0);
        }
    }


    private MemoryValue readBus(MemoryAddress memoryAddress) throws NotImplementedException, IllegalAccessException {
        for (MMUComponent mmuComponent : this.ppuBus) {
            if (mmuComponent.IsAddressed(memoryAddress)) {
                return mmuComponent.read(memoryAddress);
            }
        }
        return MemoryValue.fromValue(0xFFFF);

    }

    private void writeBus(MemoryAddress address, MemoryValue value) throws NotImplementedException {
        for (MMUComponent mmuComponent : this.ppuBus) {
            if (mmuComponent.IsAddressed(address)) {
                mmuComponent.write(address, value);
            }
        }
    }

    @Override
    public void write(MemoryAddress memoryAddress, MemoryValue value) throws NotImplementedException {

        if (memoryAddress.getValue() == IOMap.LY) {
            this.drawPointer.setLY(value.getValue());
        } else {
            writeBus(memoryAddress, value);

            // intercept writes to LCDC, because we want to know if we need to switch the Fetcher offset
            // (0=9800-9BFF, 1=9C00-9FFF)
            if(memoryAddress.getValue() == IOMap.LCDC) {
                // Disable LCDC register for now, implementation is still missing
               // handleBgTileMapSwitch(value);
            }
        }
    }

    @Override
    public MemoryValue read(MemoryAddress memoryAddress) throws NotImplementedException, IllegalAccessException {
        if (memoryAddress.getValue() == IOMap.LY) {
            return MemoryValue.fromValue(this.drawPointer.getLY());
        } else {
            return readBus(memoryAddress);
        }
    }

    @Override
    public void flush() {
        this.ppuBus = new ArrayList<>();
    }

    @Override
    public void connect(MMUComponent mmuComponent) {
        this.memoryMap.addEntry(mmuComponent);
        this.ppuBus.add(mmuComponent);
    }

    @Override
    public void disconnect(MMUComponent mmuComponent) {
        // not used
    }

    @Override
    public MemoryMap getMemoryMap() {
        return this.memoryMap;
    }

    protected void incLY() {
        this.drawPointer.incY();
        if (this.drawPointer.isEndOfVblank()) {
            this.drawPointer.setLY(0);
            this.state = PpuState.OAM_SEARCH;
            this.screen.refresh();
            this.fetcher.reset();
        }
    }

    @Override
    public boolean IsAddressed(MemoryAddress memoryAddress) throws NotImplementedException {

        for (MMUComponent mmuComponent : this.ppuBus) {
            if (mmuComponent.IsAddressed(memoryAddress)) {
                return true;
            }
        }
        return memoryAddress.getValue() == IOMap.LY;
    }

    @Override
    public List<MemoryMapEntry> getComponentIds() {
        MemoryMapEntry memoryMapEntry = new MemoryMapEntry("PPU");
        memoryMapEntry.addRegister(IOMap.LY, "LY Register");
        memoryMapEntry.addRegister(IOMap.LCDC, "LCD Control Register");

        List<MemoryMapEntry> memoryMapEntries = new ArrayList<>();
        memoryMapEntries.add(memoryMapEntry);
        return memoryMapEntries;
    }

    private void updateTileIndex() {
        this.tc += 1;
        if (this.tc == 8) {
            this.tc = 0;
            this.fetcher.updateColumn(tileIndex);
            this.tileIndex += 1;
        }
    }

    private void oamSearch() {
        // TODO: implement
    }

    private void hBlank() {
        // TODO: implement
    }
    private void vBlank() {
        this.incLY();
    }

    private void doHBlank() {
        this.screen.newScanline();
        this.incLY();
        this.fetcher.updateRow(this.drawPointer.getLY());
        this.fifo.clear();
        this.drawPointer.newScanline();
        this.tc = 0;
        this.tileIndex = 0;
    }

    private void doVBlank() {
        // Trigger VBlank interrupt
        this.state = PpuState.VBLANK;
    }

    private void pixelTransfer() throws NotImplementedException, IllegalAccessException {
        this.fetcher.tick();
        if(this.drawPointer.isEndofScanline()) {
            this.doHBlank();
        }
        else {
            if (this.fifo.isFilled()) {
                this.fifo.shift();
                this.drawPointer.incX();
                this.updateTileIndex();

            }
            if (this.fetcher.state == FetcherState.PUSH_PIXELS) {
                if (this.fifo.isReady()) {
                    List<Integer> pixels = this.fetcher.decode(this.fetcher.getData0(), this.fetcher.getData1());
                    this.fifo.pushBlock(pixels);
                    this.fetcher.state = FetcherState.READ_TILE;
                }
            }
        }
    }


    public void tick(long cycles) throws NotImplementedException, IllegalAccessException {
        // Each scanline is 456 dots (114 CPU cycles) long
        this.cycleCount += cycles / 4;

        // OAM search
        if (this.cycleCount == 20 && this.state == PpuState.OAM_SEARCH) {
            this.oamSearch();
            this.state = PpuState.PIXEL_TRANSFER;
        }
        else if (this.cycleCount > 20 && this.cycleCount <= 63 && state == PpuState.PIXEL_TRANSFER) {
            this.pixelTransfer();
        }
        else if(this.cycleCount > 63 && this.cycleCount <= 115 && this.state == PpuState.PIXEL_TRANSFER) {
            this.state = PpuState.HBLANK;
        }
        else if (this.cycleCount > 63 && this.cycleCount <= 115 && this.state == PpuState.HBLANK) {
            this.hBlank();
        }


        if (this.cycleCount >= 114) {
            this.cycleCount = this.cycleCount - 114;
            if(this.state == PpuState.HBLANK) {
                this.state = PpuState.OAM_SEARCH;
            }
            else if(state == PpuState.VBLANK) {
                this.vBlank();
            }

            else if(this.drawPointer.isStartOfVBlank()) {
                this.doVBlank();
            }
        }



    }

    public void connectToBus(MMUComponent component) {

        if(component instanceof Screen) {
            this.fifo.setScreen((Screen) component);
            this.screen = (Screen)component;
        }
        this.connect(component);
    }
}
