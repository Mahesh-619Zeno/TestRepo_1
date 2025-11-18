import config.ApiConfig;
import utils.Logger;

public class ApiClient {
    private final ApiConfig config;

    public ApiClient(ApiConfig config) {
        this.config = config;
    }

    public void fetchData() {
        Logger.info("Fetching data from API: " + config.baseUrl);
        // Dummy API call logic
        Logger.info("Data fetched successfully.");
    }
}