public class ServerPort {
    public static int getPort() {
        String portStr = System.getenv("SERVER_PORT");

        if (portStr == null || portStr.isEmpty()) {
            return 8080;
        }

        try {
            return Integer.parseInt(portStr);
        } catch (NumberFormatException e) {
            System.err.println("Warning: Invalid port number format in 'SERVER_PORT'. Using default port 8080.");
            return 8080;
        }
    }
}