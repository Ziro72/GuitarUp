import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class ChordSender {

    public static void sendChord(String jsonString) {
        try {
            URL url = new URL("http://localhost:5000/process-chord");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setDoOutput(true);
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json");

            try (OutputStream os = conn.getOutputStream()) {
                os.write(jsonString.getBytes());
                os.flush();
            }

            if (conn.getResponseCode() != HttpURLConnection.HTTP_OK) {
                throw new RuntimeException("Failed : HTTP error code : " + conn.getResponseCode());
            }

            System.out.println("Chord sent successfully.");
            conn.disconnect();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
