package gui.events;

import java.util.ArrayList;
import java.util.List;

public class EventManager {

    List<EventListener> eventListeners;

    public EventManager() {
        this.eventListeners = new ArrayList<>();
    }

    public void sendEvent(EmulatorGuiEvents guiEvents,Object payload) {

        for(EventListener eventListener : this.eventListeners) {
            eventListener.receive(guiEvents, payload);
        }
    }

    public void register(EventListener eventListener) {
        this.eventListeners.add(eventListener);
    }

}
