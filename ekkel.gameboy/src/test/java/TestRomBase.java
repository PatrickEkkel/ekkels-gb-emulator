import debugger.SerialDevice;
import testrunner.GameBoyRunner;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class TestRomBase implements SerialDevice {

    private String data = "";

    private StringBuilder stringBuilder;

    public void setupTest() throws IOException, InterruptedException {
        this.stringBuilder = new StringBuilder("");
        // first clone repo from github with testroms
        executeShell("mkdir -p /tmp/testroms");
        executeShell("git clone https://github.com/retrio/gb-test-roms.git /tmp/testroms");
    }

    public boolean isTestPassed(GameBoyRunner runner) {
        long startTime = System.currentTimeMillis(); //fetch starting time
        while((System.currentTimeMillis() - startTime) < 10000)
        {
            if(stringBuilder.toString().contains("Passed")) {
                System.out.println("Captured output...");
                System.out.print(this.stringBuilder.toString());
                System.out.print("\n");
                return true;
            }
            // do something
        }
        System.out.println("10 seconds passed, Gameboy has not responded with Passed, assuming failed state");
        System.out.println("Captured output...");
        System.out.print(this.stringBuilder.toString());
        System.out.print("\n");
        return false;
    }

    private void executeShell(String cmd) throws InterruptedException, IOException {
        Runtime run = Runtime.getRuntime();
        Process pr = run.exec(cmd);
        pr.waitFor();
        BufferedReader buf = new BufferedReader(new InputStreamReader(pr.getInputStream()));
        String line = "";
        while ((line=buf.readLine())!=null) {
            System.out.println(line);
        }
    }

    @Override
    public void logData(String data) {
        this.stringBuilder.append(data);
    }
}
