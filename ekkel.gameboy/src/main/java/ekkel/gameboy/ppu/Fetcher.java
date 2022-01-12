package ekkel.gameboy.ppu;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.mmu.*;
import ekkel.gameboy.cpu.IOMap;
import gui.GameBoyDMGPalette;

import java.util.ArrayList;
import java.util.List;

public class Fetcher {


    FetcherState state;
    private MMU mmuImpl;

    private int offset;
    private int tilemapRam;
    private int tileAddress;
    private int column;
    private int ticks;

    private int tileMapOffset = 0;
    private int bgMapOffset = 0;
    private MemoryValue data0;
    private MemoryValue data1;

    public Fetcher(MMU mmuImpl) {
        this.state = FetcherState.READ_TILE;
        this.mmuImpl = mmuImpl;
        this.column = 0;
        this.ticks = 0;
    }

    private Computable getLY() throws NotImplementedException, IllegalAccessException {
        return this.mmuImpl.read(MemoryAddress.fromValue(IOMap.LY));
    }

    private void readTile() throws NotImplementedException, IllegalAccessException {
        int currentOffset = this.offset + this.column;
        int tileId = this.mmuImpl.read(MemoryAddress.fromValue(currentOffset)).getValue();

        this.tileAddress = tilemapRam + (tileId * 16);
    }

    private void readData0() throws NotImplementedException, IllegalAccessException {
        int tileAddress = this.tileAddress;
        Computable LY = getLY();
        int o = (LY.getValue() % 8);
        o += o;
        int tileRow = tileAddress + o;
        this.data0 = this.mmuImpl.read(MemoryAddress.fromValue(tileRow));
    }

    private void readData1() throws NotImplementedException, IllegalAccessException {
        int address = tileAddress + 1;
        this.data1 = this.mmuImpl.read(MemoryAddress.fromValue(address));
    }

    public Computable getData0() {
        return this.data0;
    }

    public Computable getData1() {
        return this.data1;
    }

    public List<Integer> decode(Computable fb, Computable sb) {
        List<Integer> result = new ArrayList<>();
        for (int x = 7; x > -1; x--) {
            int msb = fb.getValue() >> x & 0x01;
            int lsb = sb.getValue() >> x & 0x01;

            if (msb == 0x01 && lsb == 0x01) {
                result.add(GameBoyDMGPalette.DARK_GREEN);
            } else if (msb != 0x01 && lsb != 0x01) {
                result.add(GameBoyDMGPalette.LIGHTEST_GREEN);
            } else if (lsb == 0x01) {
                result.add(GameBoyDMGPalette.LIGHT_GREEN);

            } else {
                result.add(GameBoyDMGPalette.DARKEST_GREEN);
            }
        }

        return result;
    }

    public void reset() {
        this.state = FetcherState.READ_TILE;
        this.tilemapRam = tileMapOffset;
        this.offset = bgMapOffset;
        this.tileAddress = 0;
        this.column = 0;
        this.ticks = 0;
    }

    public void setOffset(int offset) {
        this.offset = offset;
        this.bgMapOffset = offset;
    }

    public void setTilemapRam(int tmr) {
        this.tilemapRam = tmr;
        this.tileMapOffset = tmr;
    }


    public void updateColumn(int scx) {
        this.column = scx;
    }

    public void updateRow(int scy) {
        if (scy % 8 == 0 && scy != 0) {
            this.offset += 32;
        }
    }

    public void tick() throws NotImplementedException, IllegalAccessException {
        ticks += 1;
        if (this.ticks < 2) {
            return;
        }
        this.ticks = 0;
        switch (state) {
            case READ_TILE:
                readTile();
                this.state = FetcherState.READ_DATA_0;
                break;
            case READ_DATA_0:
                readData0();
                this.state = FetcherState.READ_DATA_1;
                break;
            case READ_DATA_1:
                readData1();
                this.state = FetcherState.PUSH_PIXELS;
                break;
        }
    }


}
