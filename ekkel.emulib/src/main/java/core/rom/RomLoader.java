package core.rom;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.lang.reflect.InvocationTargetException;

public class RomLoader<T extends Rom> {

    public T load(String path, Class<T> clazz) {
        try {
            InputStream inputStream = new FileInputStream(path);
            T result = clazz.getDeclaredConstructor().newInstance();
            result.setRomContents(inputStream.readAllBytes());
            return result;

        } catch (InstantiationException
                | IOException
                | NoSuchMethodException
                | InvocationTargetException
                | IllegalAccessException e) {
            e.printStackTrace();
        }
        return null;
    }

}
