public class MainRunner {
    public static void main(String[] args) {
        try {
            String dbConn = DatabaseConfig.getConnectionString();
            System.out.println("Database connection string obtained.");
        } catch (IllegalStateException e) {
            System.err.println(e.getMessage());
        }

        int port = ServerPort.getPort();
        System.out.println("Server will run on port: " + port);

        boolean enabled = FeatureToggle.isFeatureEnabled();
        System.out.println("Feature toggle status: " + (enabled ? "Enabled" : "Disabled"));

        EnvironmentLister.printAll();
    }
}