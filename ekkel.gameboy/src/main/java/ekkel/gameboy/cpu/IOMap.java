package ekkel.gameboy.cpu;

// Registers and documentation taken from http://www.codeslinger.co.uk/pages/projects/gameboy/graphics.html

public class IOMap {
    // Interrupt Enable IO
    public static int IE = 0xFFFF;

    // Serial Interface
    public static int SC = 0xFF02;
    public static int SB = 0xFF01;

    // Timer Control
    public static int TAC = 0xFF07;
    //  LCD Control Register
    public static int LCDC = 0xFF40;
    // STAT Control Register
    public static int STAT = 0xFF41;
    // The Y Position of the BACKGROUND
    public static int SCROLLY = 0xFF42;
    // The X Position of the BACKGROUND
    public static int SCROLLX = 0xFF43;
    // The Y Position of the VIEWING AREA to start drawing the window from
    public static int WINDOWY = 0xFF4A;
    // The X Positions -7 of the VIEWING AREA to start drawing the window from
    public static int WINDOWX = 0xFF4B;


    // Current line that is being drawn
    public static int LY = 0xFF44;
    // CGB CPU Only
    public static int KEY1 = 0xFF4D;

    // Write to this register to unmap off internal Boot ROM
    public static int DMGROMDISABLE = 0xFF50;



}
