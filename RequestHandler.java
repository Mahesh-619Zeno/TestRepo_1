public class RequestHandler {

    public void handleRequest(String params, String options) {
        System.out.println("Handling request with:");
        System.out.println("Params: " + params);
        System.out.println("Options: " + options);
    }

    public String processData(String data) {
        // Process and return modified data
        return "Processed: " + data.trim();
    }

    public static void main(String[] args) {
        RequestHandler handler = new RequestHandler();

        String params = "userId=123";
        String options = "verbose=true";
        String data = "   raw input   ";

        handler.handleRequest(params, options);
        String result = handler.processData(data);

        System.out.println(result);
    }
}
