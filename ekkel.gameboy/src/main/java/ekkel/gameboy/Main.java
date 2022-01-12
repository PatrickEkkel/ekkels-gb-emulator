package ekkel.gameboy;

import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.registers.Registers;
import core.mmu.ComputableImpl;
import debugger.*;
import debugger.client.consoleDebugger.ConsoleDebugger;
import debugger.client.traceLogger.Tracer;
import ekkel.gameboy.app.GameBoyMain;
import gui.*;
import gui.menuitems.LoadRomMenuItem;

import java.io.IOException;


public class Main {

    public static void main(String[] args) throws IOException {
        AppWindow appWindow = new AppWindow("JavaGB");
        appWindow.addMenu("File");

        GameBoyMain gameBoyMain = new GameBoyMain();
        appWindow.getEventManager().register(gameBoyMain);

        appWindow.addMenuItem("File", new LoadRomMenuItem("Load ROM"));
        // Gameboy gameboy = new Gameboy(false);
        gameBoyMain.getGameboy().connectLinkCable(new SerialConsoleLogger());

        Tracer tracer = new Tracer("/tmp/trace_coffeegb.log",true,gameBoyMain.getGameboy());

       // appWindow.setDisplayDevice(gameBoyMain.getGameboy());
       // appWindow.start();

        DebugOptions debugOptions = new DebugOptions();
        debugOptions.setEnableDebug(false);
        debugOptions.setEmitProgramCounter(true);
        debugOptions.setDisableCpu(false);
        debugOptions.setEmitCurrentOpcode(true);
        debugOptions.setEmitClockcycles(false);
        debugOptions.setEmitRegisters(true);
        debugOptions.setEmitExternalRegisters(true);
        //ConsoleDebugger debugger = new ConsoleDebugger(debugOptions);

        DebuggerBridge debuggerClient = new DebuggerBridge(gameBoyMain.getGameboy().getCPU(), tracer, gameBoyMain.getGameboy().getClock(), gameBoyMain.getGameboy().getMMU());


        debuggerClient.setCpuInit(cpu -> {
            cpu.writeRegister(Registers.AF, new ComputableImpl(0x1180));
            cpu.writeRegister(Registers.BC, new ComputableImpl(0x0000));
            cpu.writeRegister(Registers.DE, new ComputableImpl(0xFF56));
            cpu.writeRegister(Registers.HL, new ComputableImpl(0x000D));
            cpu.writeRegister(Registers.SP, new ComputableImpl(0xFFFE));
        });
        gameBoyMain.getGameboy().attachDebugger(debuggerClient);

        // gameBoyMain.getGameboy().load("/home/patrick/Git/github/javagb/ekkel.gameboy/testroms/03-op_sp_hl.gb");
        //gameBoyMain.getGameboy().load("/home/patrick/Git/github/javagb/ekkel.gameboy/testroms/06-ldrr.gb");
         gameBoyMain.getGameboy().load("/home/patrick/Git/github/javagb/ekkel.gameboy/testroms/04_r_imm.gb");

         gameBoyMain.getGameboy().powerOn();
        /*
        Disassembler disassembler = new Disassembler(gameboy.getMMU(),gameboy.getCPU());
        try {
            disassembler.run(new GameboyDissassemblerConfig());
        } catch (MemoryRegionDescriptionNotFound | IllegalAccessException | UnknownOpcodeException memoryRegionDescriptionNotFound) {
            memoryRegionDescriptionNotFound.printStackTrace();
        }*/


        // Debugger window
        //   DebuggerWindow debuggerWindow = new DebuggerWindow("Gameboy debugger");
        //  debuggerWindow.start();

    }
}
