import org.herac.tuxguitar.io.base.*;
import org.herac.tuxguitar.io.gtp.*;
import org.herac.tuxguitar.song.factory.TGFactory;
import org.herac.tuxguitar.song.models.*;
import org.herac.tuxguitar.util.TGContext;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        String filePath = "src/main/java/forbidden_friendship.gpx";
        SongReader.read(filePath);
    }
}

class SongReader {

    public static void read(String filePath) {
        try (InputStream inputStream = new FileInputStream(filePath)) {
            TGContext context = new TGContext();

            // Подключение всех плагинов для GP1-GP5
            new GP1InputStreamPlugin().connect(context);
            new GP2InputStreamPlugin().connect(context);
            new GP3InputStreamPlugin().connect(context);
            new GP4InputStreamPlugin().connect(context);
            new GP5InputStreamPlugin().connect(context);

            // Подключение плагинов для GPX v6 и v7
            new org.herac.tuxguitar.io.gpx.v6.GPXInputStreamPlugin().connect(context);
            new org.herac.tuxguitar.io.gpx.v7.GPXInputStreamPlugin().connect(context);

            TGFactory factory = new TGFactory();
            TGSongReaderHandle handle = new TGSongReaderHandle();
            handle.setInputStream(inputStream);
            handle.setFactory(factory);

            TGFileFormatManager manager = TGFileFormatManager.getInstance(context);
            manager.read(handle);

            TGSong song = handle.getSong();

            if (song != null) {
                extractAndSendChords(song);
            } else {
                System.err.println("Failed to read the song.");
            }
        } catch (Exception e) {
            System.err.println("Error processing file: " + e.getMessage());
        }
    }

    private static void extractAndSendChords(TGSong song) {
        var trackIterator = song.getTracks();
        while (trackIterator.hasNext()) {
            TGTrack track = trackIterator.next();

            var measureIterator = track.getMeasures();
            while (measureIterator.hasNext()) {
                TGMeasure measure = measureIterator.next();

                for (TGBeat beat : measure.getBeats()) {
                    if (beat.isChordBeat()) {
                        TGChord chord = beat.getChord();

                        // Формируем JSON для аккорда
                        JsonObject chordJson = new JsonObject();
                        chordJson.addProperty("name", chord.getName());
                        chordJson.addProperty("start_fret", chord.getFirstFret());

                        // Barre
                        int barreFret = getBarreFret(chord.getStrings());
                        chordJson.addProperty("barre", barreFret);

                        // Fingers
                        JsonArray fingersJson = new JsonArray();
                        addFingersToJson(chord.getStrings(), barreFret, fingersJson);
                        chordJson.add("fingers", fingersJson);

                        // Отправка JSON на сервер
                        sendChordToServer(chordJson);
                    }
                }
            }
        }
    }

    private static int getBarreFret(int[] frets) {
        Map<Integer, Integer> fretCount = new HashMap<>();
        for (int fret : frets) {
            if (fret > 0) {
                fretCount.put(fret, fretCount.getOrDefault(fret, 0) + 1);
            }
        }

        // Находим лад с максимальным количеством струн
        int maxCount = 0;
        int barreFret = 0;
        for (Map.Entry<Integer, Integer> entry : fretCount.entrySet()) {
            if (entry.getValue() > maxCount) {
                maxCount = entry.getValue();
                barreFret = entry.getKey();
            }
        }

        return maxCount > 1 ? barreFret : 0;
    }

    private static void addFingersToJson(int[] frets, int barreFret, JsonArray fingersJson) {
        for (int string = 1; string <= frets.length; string++) {
            int fret = frets[string - 1];
            if (fret > 0 && fret != barreFret) {
                JsonObject fingerJson = new JsonObject();
                fingerJson.addProperty("number", string);
                fingerJson.addProperty("fret", fret);
                fingerJson.addProperty("string", string);
                fingersJson.add(fingerJson);
            }
        }
    }

    private static void sendChordToServer(JsonObject chordJson) {
        try {
            // Устанавливаем соединение с сервером
            URL url = new URL("http://localhost:5000/process-chord");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json");
            connection.setDoOutput(true);

            // Отправляем JSON
            try (OutputStream os = connection.getOutputStream()) {
                os.write(chordJson.toString().getBytes());
                os.flush();
            }

            // Читаем ответ от сервера
            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                System.out.println("Chord sent successfully: " + chordJson.get("name").getAsString());
            } else {
                System.err.println("Failed to send chord. Response code: " + responseCode);
            }

        } catch (IOException e) {
            System.err.println("Error sending chord to server: " + e.getMessage());
        }
    }
}
