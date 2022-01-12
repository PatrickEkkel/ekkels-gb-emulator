package core.binary.eightbit;

public class Arithmatic {


    private static boolean isDecHalfCarry(int a, int b) {
        return false;
    }

    private static boolean isAddHalfCarry(int a, int b) {
        return false;
    }

    public static boolean isHalfCarry(int a, int b, AluOperation operation) {

        switch (operation) {

            case ADD:
                return isAddHalfCarry(a,b);
            case SUBSTRACT:
                return isDecHalfCarry(a,b);
        }
        return false;
    }

}
