package gui;

import java.awt.*;

public class GameBoyDMGPalette extends Palette {


    public static int DARKEST_GREEN = 3;
    public static int DARK_GREEN = 2;
    public static int LIGHT_GREEN = 1;
    public static int LIGHTEST_GREEN = 0;
    public static int WHITE = 4;

    public GameBoyDMGPalette() {
        this.colors = new int[] {0xe6f8da, 0x99c886, 0x437969, 0x051f2a, Color.WHITE.getRGB()};
    }

}
