
import config.DatabaseConfig;
import utils.Logger;

public class DatabaseService {
    private final DatabaseConfig config;

    public DatabaseService(DatabaseConfig config) {
        this.config = config;
    }

    public void connect() {
        Logger.info("Attempting to connect to database at " + config.host + ":" + config.port);
        // Dummy connection logic
        Logger.info("Database connection successful.");
    }
}