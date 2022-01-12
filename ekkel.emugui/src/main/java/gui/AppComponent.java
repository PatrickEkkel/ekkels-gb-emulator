package gui;

import javax.swing.*;
import java.awt.*;

public class AppComponent extends JPanel implements Runnable {

    protected int width;
    protected int height;


    public void setSize(int width, int height) {
        this.width = width;
        this.height = height;
        this.setPreferredSize(new Dimension(width, height));
    }

    public AppComponent() {
        super();
    }


    @Override
    public void run() {

    }
}
