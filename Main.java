public class Main {
    public static void main(String[] args) {
        String apiKey = System.getenv("API_KEY");

        if (apiKey != null && !apiKey.isEmpty()) {
            System.out.println("API Key is set.");
        } else {
            System.out.println("API Key is not set. Please set the 'API_KEY' environment variable.");
        }
    }
}