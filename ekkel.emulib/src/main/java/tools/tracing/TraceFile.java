package tools.tracing;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Scanner;

public class TraceFile {

    private Scanner fileScanner;
    private String filename;
    private BufferedWriter writer;
    private TraceFormat traceFormat;

    private String currentContents;

    private String previousContents;

    public TraceFile(TraceFormat traceFormat, String filename) {
        this.filename = filename;
        this.traceFormat = traceFormat;
    }
    public void create() throws IOException {
       this.writer = new BufferedWriter(new FileWriter("/tmp/javagb_tracer.log"));
    }
    public void load() throws FileNotFoundException {
        FileInputStream inputStream = new FileInputStream(filename);
        this.fileScanner = new Scanner(inputStream, "UTF-8");
    }

    public void write(CPUState cpuState) throws IOException {
        String contents = null;
        try {
            contents = this.traceFormat.parse(cpuState);
            this.previousContents = this.currentContents;
            this.currentContents = contents;
            if(this.writer != null) {
                this.writer.write(String.format("%s\n", contents));
            }

        } catch (Exception e) {
            System.out.printf("error: %s%n", e);
        }
    }

    public void skipLines(int lines) {
        for (int i = 0; i < lines; i++) {
            fileScanner.nextLine();
        }
    }

    public boolean hasNextLine() {
        return this.fileScanner.hasNextLine();
    }

    public TraceLine getNextLine() {

        if(this.fileScanner != null) {

            String nextLine = this.fileScanner.nextLine();
            this.previousContents = this.currentContents;
            this.currentContents = nextLine;
            return new TraceLine(this.traceFormat,this.currentContents);
        }
        else {
            return new TraceLine(this.traceFormat,this.currentContents);
        }
    }

    public String getPreviousContents() {
        return this.previousContents;
    }
    public String getCurrentContents() {
        return this.currentContents;
    }

    public TraceFile copy(String copiedFilename) throws IOException {
        Path copied = Paths.get(copiedFilename);
        Path orginalPath = new File(filename).toPath();
        Files.copy(orginalPath, copied, StandardCopyOption.REPLACE_EXISTING);
        TraceFile result = new TraceFile(this.traceFormat,copiedFilename);
        result.load();
        return result;
    }

    public void close() throws IOException {
        this.writer.close();
    }





}
