public class DatabaseConfig {
    public static String getConnectionString() {
        String connStr = System.getenv("DB_CONNECTION_STRING");
        
        if (connStr == null || connStr.isEmpty()) {
            throw new IllegalStateException("Required environment variable 'DB_CONNECTION_STRING' is not set.");
        }
        
        return connStr;
    }
}