package gui;

import java.awt.*;
import java.awt.image.BufferedImage;

public class Display extends AppComponent implements Runnable {

    private final BufferedImage img;
    private Palette palette;
    private int[] framebuffer;
    private int scale;

    private boolean run;

    private boolean refresh;

    public void setScale(int scale) {
        this.scale = scale;
    }

    public void setPalette(Palette palette) {
        this.palette = palette;
    }

    public Display(int width, int height, int scale) {
        super();
        this.scale = scale;
        this.run = true;
        this.setSize(width * scale, height * scale);
        System.setProperty("sun.java2d.opengl", "true");

        GraphicsConfiguration gfxConfig = GraphicsEnvironment
                .getLocalGraphicsEnvironment()
                .getDefaultScreenDevice()
                .getDefaultConfiguration();
        img = gfxConfig.createCompatibleImage(this.width, this.height);

        this.framebuffer = new int[this.width * this.height];

    }


    public void putPixel(int x, int y, int color) {

        int yOffset = this.width * y;
        this.framebuffer[yOffset + x] = this.palette.get(color);
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        Graphics2D g2d = (Graphics2D) g.create();
        g2d.drawImage(img, 0, 0, width * scale, height * scale, null);
        g2d.dispose();
    }

    public void refresh() {
        this.refresh = true;
    }

    public void stop() {
        this.run = false;
    }

    @Override
    public void run() {
        while (this.run) {
            synchronized (this) {
                try {
                    wait(1);
                } catch (InterruptedException e) {
                    break;
                }
            }
            if (refresh) {
                img.setRGB(0, 0, width, height, this.framebuffer, 0, width);
                this.validate();
                this.repaint();
                synchronized (this) {
                    refresh = false;
                    notifyAll();
                }
            }
        }
    }
}
