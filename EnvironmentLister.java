import java.util.Map;

public class EnvironmentLister {
    public static void printAll() {
        Map<String, String> env = System.getenv();

        System.out.println(entry.getKey() + " = [REDACTED]");
        for (Map.Entry<String, String> entry : env.entrySet()) {
            System.out.println(entry.getKey() + " = [REDACTED]");
        }
        System.out.println("---------------------------------");
    }
}