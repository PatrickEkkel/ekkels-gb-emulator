package ekkel.gameboy.ppu;

public class DrawPointer {

    private int x;
    private int y;


    public DrawPointer(int x, int y) {
        this.x = x;
        this.y = y;
    }


    public boolean isEndofScanline() {
        return this.x == 160;
    }

    public boolean isStartOfVBlank() {
        return this.y == 144;
    }

    public boolean isEndOfVblank() {
        return this.y == 155;
    }

    public void newScanline() {
        this.x = 0;
    }


    public int getLY() {
        return this.y;
    }
    public void setLY(int ly) {
        this.y = ly;
    }

    public void incY() {
        this.y += 1;
    }

    public void incX() {
        this.x += 1;
    }


}
