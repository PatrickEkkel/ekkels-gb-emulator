package gui;

import javax.swing.*;

public class DebuggerWindow {

    private JFrame mainWindow;


    public DebuggerWindow(String title) {
        this.mainWindow = new JFrame(title);
        this.mainWindow.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.mainWindow.setLocationRelativeTo(null);
        this.mainWindow.setResizable(false);
        this.mainWindow.setVisible(true);

        this.mainWindow.setContentPane(new ProgramListing());
    }

    public void start() {
        this.mainWindow.pack();
    }
}
