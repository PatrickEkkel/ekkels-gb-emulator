package debugger.client.traceLogger;

import core.cpu.CPU;
import core.cpu.opcodes.Opcode;
import core.cpu.opcodes.exceptions.DivergedCPUStateException;
import core.cpu.opcodes.exceptions.NotImplementedException;
import core.cpu.opcodes.exceptions.UnknownOpcodeException;
import core.cpu.registers.Register;
import core.cpu.registers.Registers;
import core.device.SimpleDevice;
import core.mmu.MMU;
import core.mmu.MMUImpl;
import debugger.DebugOptions;
import debugger.client.DebuggerClient;
import tools.tracing.*;
import tools.tracing.TraceLine;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.*;

public class Tracer extends tools.tracing.Tracer implements DebuggerClient {

    private final TraceFile referenceFile;
    private final TraceFile sourceFile;

    int opcodeCounter;

   // String registers = "";
    Integer opcode = 0;
    int skipLines = 0;
    boolean patternFound;


    private List<String> exclusions;

    private boolean breakOnDifference;

    private boolean logToFile;

    List<OpcodePattern> opcodePatterns;


    public void setBreakonDifference(boolean breakonDifference) {
        this.breakOnDifference = breakonDifference;
    }

    public void setLogToFile(boolean logToFile) {
        this.logToFile = logToFile;
    }

    public void addExclusion(String address) {
        this.exclusions.add(address);
    }

    public Tracer(String filename, boolean logToFile, SimpleDevice device) throws IOException {
        super(new TraceFormat() {
            @Override
            public String getLineFormat() {
                return "C:%s;PC:%s;OPCODE:%s;HL:%s;AF:%s;BC:%s;DE:%s;SP:%s;";
            }

            @Override
            public String getElementSeperator() {
                return ";";
            }

            @Override
            public String getTraceElementSeperator() throws Exception {
                return ":";
            }

            @Override
            public int getPCIndex() throws Exception {
                return 1;
            }

            @Override
            public int getOpcodeIndex() throws Exception {
                return 2;
            }

            @Override
            public int getOpcodeCounterIndex() throws Exception {
                return 0;
            }

            @Override
            public String parse(CPUState cpuState) {
               Map<String, Register> registers = cpuState.getRegisters();
               return String.format(this.getLineFormat(), cpuState.getOpcodeCounter(),
                       TraceLine.toHex(cpuState.getPc()),
                       TraceLine.toHex(cpuState.getOpcode()),
                       registers.get("HL"),
                       registers.get("AF"),
                       registers.get("BC"),
                       registers.get("DE"),
                       registers.get("SP"));
            }
        });
        this.referenceFile = new TraceFile(this.getTraceFormat(),filename);
        this.sourceFile = new TraceFile(this.getTraceFormat(),"/tmp/javagb_tracer.log");
        this.referenceFile.load();

        this.opcodeCounter = 0;
       // this.loadTraceFile(filename);

        if (logToFile) {
           // this.writer = new BufferedWriter(new FileWriter("/tmp/javagb_tracer.log"));
            this.sourceFile.create();
        }
        this.logToFile = logToFile;
        this.exclusions = new ArrayList<>();
        this.opcodePatterns = new ArrayList<>();
        this.patternFound = false;
        this.preProcessTraceFile(filename);
    }

    public void addOpcodePattern(OpcodePattern opcodePattern) {
        this.opcodePatterns.add(opcodePattern);
    }

    private void preProcessTraceFile(String filename) throws IOException {
        // make copy of original tracefile
        TraceFile copiedTracefile = this.referenceFile.copy("/tmp/coffeegb.temp");

        while (copiedTracefile.hasNextLine()) {
           TraceLine currentLine = copiedTracefile.getNextLine();
            // get opcode
           String opcodeValue =  currentLine.getElement(2).getValue();
           //String opcode = currentLine.split(";")[2];
           //String opcodeValue = opcode.split(":")[1];
        }
    }
    @Override
    public void debug(CPU cpu) {
        try {
            Opcode opcode = cpu.getFetcher().fetch().decode();
          //  this.PC = cpu.readRegister(Registers.PC);
          //  this.opcode = opcode.getInstr();
            this.setCpuState(new CPUState(cpu.readRegister(Registers.PC).getValue(),opcode.getInstr(), opcodeCounter));
        } catch (UnknownOpcodeException | NotImplementedException | IllegalAccessException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void printCPUState(CPU cpu) {
        Map<String, Register> registers = new HashMap<>();
        registers.put("SP", cpu.readRegister(Registers.SP));
        registers.put("AF", cpu.readRegister(Registers.AF));
        registers.put("BC", cpu.readRegister(Registers.BC));
        registers.put("DE", cpu.readRegister(Registers.DE));
        registers.put("HL",cpu.readRegister(Registers.HL));
        this.getCpuState().setRegisters(registers);
    }

    @Override
    public void printClockCycles(long clockCycles) {

    }

    @Override
    public void printRegisters(MMUImpl mmuImpl) {

        for (OpcodePattern opcodePattern : this.opcodePatterns) {

            if (opcodePattern.isPatternDetected(mmuImpl, this.getCpuState().getPc())) {
                this.skipLines = opcodePattern.getOpcodes().size();
                System.out.printf("Opcode pattern found, skipping %d lines.\n", this.skipLines);
                this.patternFound = true;
            }

        }
    }

    @Override
    public void modifyCpuState(CPU cpu) {
        // TODO: maybe remove this method.

    }
    private void skipTraceFileforward() {
        this.referenceFile.skipLines(this.skipLines);
    }

    private boolean skipComparison() {
        if (this.skipLines > 0) {
            this.skipLines -= 1;
            return true;
        }
        return false;
    }

    @Override
    public void wrapUp() throws DivergedCPUStateException {

        // check if there is a match found..
        if (this.patternFound) {
            this.patternFound = false;
            skipTraceFileforward();
        }
      //  String currentState = String.format("C:%s;PC:%s;OPCODE:0x%S;%s\n", opcodeCounter, PC, Integer.toHexString(opcode), registers);
        //if (this.logToFile) {
         //   try {
        try {
            this.sourceFile.write(this.getCpuState());
        } catch (IOException e) {
            e.printStackTrace();
        }
        //  this.writer.write(currentState);
          //  } catch (IOException e) {
            //    e.printStackTrace();
           // }
        //}

        if (!this.skipComparison() && this.referenceFile.hasNextLine()) {
          //  TraceLine expectedState = this.referenceFile.getNextLine();

            List<String> differences = new ArrayList<>();
            if (this.breakOnDifference) {

                this.getTraceComparator().compare(sourceFile,referenceFile);
                differences = this.getTraceComparator().getResults();
                
               // differences = compareTraceLines(expectedState, currentState);
            }

            if (!differences.isEmpty() && this.breakOnDifference) {
                String message = "\n";
                for (String m : differences) {
                    message += m + "\n";
                }
                try {
                    if (this.logToFile) {
                        this.sourceFile.close();
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
                message += "reference previous state: " + this.referenceFile.getPreviousContents() + "\n";
                message += "source previous state: " + this.sourceFile.getPreviousContents() + "\n";

                throw new DivergedCPUStateException(message);

            }

        }
        opcodeCounter += 1;
    }

    @Override
    public DebugOptions getDebugOptions() {
        DebugOptions debugOptions = new DebugOptions();
        debugOptions.setEnableDebug(true);
        return debugOptions;
    }
}
