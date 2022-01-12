package gui;

import gui.events.EventManager;

import javax.swing.*;

public class AppMenuItem {

    private JMenuItem jMenuItem;


    private AppWindow parent;
    public AppMenuItem(String name) {
        this.jMenuItem = new JMenuItem(name);
    }

    protected EventManager getEventManager() {
        return this.parent.getEventManager();
    }
    public void setParent(AppWindow parent) {
        this.parent = parent;
    }

    public JMenuItem getJMenuItem() {
        return jMenuItem;
    }
}
