package ekkel.gameboy.app;

import ekkel.gameboy.Gameboy;
import gui.events.EmulatorGuiEvents;
import gui.events.EventListener;

public class GameBoyMain extends Thread implements EventListener {

    private Gameboy gameboy;


    public GameBoyMain() {
        this.gameboy = new Gameboy(false);
    }

    public Gameboy getGameboy() {
        return this.gameboy;
    }

    @Override
    public void receive(EmulatorGuiEvents events, Object payload) {


        if (events == EmulatorGuiEvents.LOADROM) {
            gameboy.load((String)payload);
            this.start();
        }
    }


    @Override
    public void run() {
        gameboy.powerOn();
    }
}
