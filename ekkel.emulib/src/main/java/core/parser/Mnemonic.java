package core.parser;

import java.util.ArrayList;
import java.util.List;

public class Mnemonic {
    private String instruction;
    public Mnemonic(String instruction) {

        this.instruction = instruction;
    }
    public List<String> getArguments() {
        List<String> result = new ArrayList<>();
        String [] elements = instruction.split(" ");
        for(int i=1;i<elements.length;i++) {
            result.add(elements[i]);
        }
        return result;
    }
    public String getInstruction() {
        List<String> arguments = this.getArguments();
        if(arguments.isEmpty()) {
            return instruction.split(" ")[0];
        }
        else {
            String result = instruction.split(" ")[0];
            for(String argument : arguments) {
                // exclude data portion
                if(ArgumentClassifier.is16BitValue(argument)) {
                    result += " " + "nnnn";
                }
                if(ArgumentClassifier.is8BitValue(argument)) {
                    result += " " + "nn";
                }
                else if(ArgumentClassifier.isRegister(argument)) {
                    result += " " + argument;
                }
                else if(ArgumentClassifier.is8BitSignedValue(argument)) {
                    result += " "  + "s8";
                }
            }
            return result;
        }


        // split on space

    }

}
