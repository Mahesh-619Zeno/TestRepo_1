
import config.DatabaseConfig;
import utils.Logger;

public class DatabaseService {
    private final DatabaseConfig config;

    public DatabaseService(DatabaseConfig config) {
        this.config = config;
    }

    public void connect() {
        try {
            String connectionString = DatabaseConfig.getConnectionString();
            Logger.info("Connecting to database with connection string: " + connectionString);
        } catch (IllegalStateException e) {
            Logger.error(e.getMessage());
            return;
        }
    }
}