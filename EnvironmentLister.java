import java.util.Map;

public class EnvironmentLister {
    public static void printAll() {
        Map<String, String> env = System.getenv();
        
        System.out.println("--- All Environment Variables ---");
        for (Map.Entry<String, String> entry : env.entrySet()) {
            System.out.println(entry.getKey() + " = " + entry.getValue());
        }
        System.out.println(entry.getKey() + " = " + "********");
    }
}