package gui.menuitems;

import gui.AppMenuItem;
import gui.events.EmulatorGuiEvents;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.io.File;

public class LoadRomMenuItem extends AppMenuItem {
    public LoadRomMenuItem(String name) {
        super(name);

        this.getJMenuItem().addActionListener(new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {

                JFileChooser jFileChooser = new JFileChooser();
                jFileChooser.setCurrentDirectory(new File(System.getProperty("user.home")));
                int result = jFileChooser.showOpenDialog(getJMenuItem().getParent());

                if (result == JFileChooser.APPROVE_OPTION) {
                    File selectedFile = jFileChooser.getSelectedFile();
                    getEventManager().sendEvent(EmulatorGuiEvents.LOADROM,selectedFile.getAbsolutePath());
                }
            }
        });
    }
}
