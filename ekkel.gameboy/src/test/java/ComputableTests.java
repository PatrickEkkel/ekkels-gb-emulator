import core.mmu.Computable;
import core.mmu.ComputableImpl;
import org.junit.jupiter.api.Test;

public class ComputableTests {


    @Test
    public void testGetBitlsb() {
        ComputableImpl value = new ComputableImpl(0x01);
        assert value.getBit(0);
    }

    @Test
    public void testGetBitmsb() {
        ComputableImpl value = new ComputableImpl(0x80);
        assert value.getBit(7);
    }

    @Test
    public void testBitlsb() {
        ComputableImpl value = new ComputableImpl(0x00);
        Computable result = value.setBit(0, 0x01);
        assert result.getValue() == 0x01;
    }
    @Test
    public void testBitmsb() {
        ComputableImpl value = new ComputableImpl(0x00);
        Computable result = value.setBit(7, 0x01);
        assert result.getValue() == 0x80;
    }
    @Test
    public void testlsbMsb() {
        ComputableImpl value = new ComputableImpl(0x01);
        Computable result = value.setBit(7, 0x01);
        assert result.getValue() == 0x81;
    }
    @Test
    public void testSetAllBits() {

        ComputableImpl value = new ComputableImpl(0x01);
        Computable result = value.setBit(7, 0x01);
        result = result.setBit(6,1);
        result = result.setBit(5,1);
        result = result.setBit(4,1);
        result = result.setBit(3,1);
        result = result.setBit(2,1);
        result = result.setBit(1,1);
        result = result.setBit(0,1);

     //   assert result.getValue() == 0x81;

        assert result.getValue() == 0xFF;
    }



}
