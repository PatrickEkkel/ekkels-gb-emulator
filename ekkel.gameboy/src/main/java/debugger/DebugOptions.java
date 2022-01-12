package debugger;

import java.util.ArrayList;
import java.util.List;

public class DebugOptions {

    private List<BreakPoint> breakPoints = new ArrayList<>();
    private boolean enableDebug;
    private boolean emitProgramCounter;
    private boolean emitCurrentOpcode;
    private boolean disableCpu;
    private boolean emitRegisters;
    private boolean emitClockcycles;
    private boolean emitExternalRegisters;

    public void setEnableDebug(boolean enableDebug) {
        this.enableDebug = enableDebug;
    }

    public boolean isEnableDebug() {
        return enableDebug;
    }

    public List<BreakPoint> getBreakPoints() {
        return this.breakPoints;
    }

    public void setEmitProgramCounter(boolean emitProgramCounter) {
        this.emitProgramCounter = emitProgramCounter;
    }

    public void setEmitCurrentOpcode(boolean emitCurrentOpcode) {
        this.emitCurrentOpcode = emitCurrentOpcode;
    }

    public void setEmitRegisters(boolean emitRegisters) {
        this.emitRegisters = emitRegisters;
    }

    public void setDisableCpu(boolean disableCpu) {
        this.disableCpu = disableCpu;
    }

    public boolean isDisableCpu() {
        return this.disableCpu;
    }

    public boolean isEmitRegisters() {
        return emitRegisters;
    }

    public boolean isEmitCurrentOpcode() {
        return emitCurrentOpcode;
    }

    public boolean isEmitProgramCounter() {
        return this.emitProgramCounter;
    }

    public DebugOptions() {

    }

    public void addBreakpoint(int pcValue) {
        this.breakPoints.add(new BreakPoint(pcValue));
    }


    public boolean isEmitClockcycles() {
        return emitClockcycles;
    }

    public void setEmitClockcycles(boolean emitClockcycles) {
        this.emitClockcycles = emitClockcycles;
    }

    public boolean isEmitExternalRegisters() {
        return emitExternalRegisters;
    }

    public void setEmitExternalRegisters(boolean emitExternalRegisters) {
        this.emitExternalRegisters = emitExternalRegisters;
    }
}
