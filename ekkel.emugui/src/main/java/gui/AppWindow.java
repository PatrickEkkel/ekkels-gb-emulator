package gui;

import gui.events.EventManager;

import javax.swing.*;
import java.util.HashMap;

public class AppWindow {


    private AppComponent appComponent;
    private EventManager eventManager;
    private JFrame mainWindow;
    private JMenuBar menuBar;

    private HashMap<String, JMenu> menus;

    public AppWindow(String title) {
        this.menus = new HashMap<>();
        this.mainWindow = new JFrame(title);
        this.menuBar = new JMenuBar();
        this.mainWindow.setJMenuBar(this.menuBar);
        this.mainWindow.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.mainWindow.setLocationRelativeTo(null);
        this.mainWindow.setResizable(false);
        this.mainWindow.setVisible(true);
        this.eventManager = new EventManager();
    }

    public void setDisplayDevice(DisplayDevice display) {
        this.mainWindow.setContentPane(display.getDisplay());
        this.appComponent = display.getDisplay();
    }

    public void start() {
        this.mainWindow.pack();
        new Thread(appComponent).start();
    }

    public void addMenu(String menuName) {
        JMenu newMenu = new JMenu(menuName);
        this.menus.put(menuName, newMenu);
        this.menuBar.add(newMenu);
    }

    public JFrame getJFrame() {
        return this.mainWindow;
    }

    public EventManager getEventManager() {
        return this.eventManager;
    }


    public void addMenuItem(String name, AppMenuItem appMenuItem) {
        appMenuItem.setParent(this);
        this.menus.get(name).add(appMenuItem.getJMenuItem());
    }

}
