package core.cpu;

public class Clock {

    private long cycle;
    private long clockspeed;
    public Clock(int clockspeed) {
        this.clockspeed = clockspeed;
    }

    public void update(int cycle) {
        this.cycle += cycle;
    }

    public long getCycle() {
        return this.cycle;
    }


    public void reset() {
        this.cycle = 0;
    }

    /**
     * Get the max Cycles we can process before we need to draw to screen
     * @return
     */
    public long getMaxCyclesPerUpdate() {
        return this.clockspeed/60;
    }

}
