public class FeatureToggle {
    public static boolean isFeatureEnabled() {
        String toggle = System.getenv("FEATURE_TOGGLE_ENABLED");

        return "true".equalsIgnoreCase(toggle) || "1".equals(toggle);
    }
}