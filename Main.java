import org.herac.tuxguitar.io.base.*;
import org.herac.tuxguitar.io.gtp.*;
import org.herac.tuxguitar.song.factory.TGFactory;
import org.herac.tuxguitar.song.models.*;
import org.herac.tuxguitar.util.TGContext;
import com.google.gson.Gson;
import com.google.gson.JsonObject;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;

public class Main {
  public static void main(String[] args) {
    String filePath = "forbidden_friendship.gpx";
    SongReader.read(filePath);
  }
}

class SongReader {

  public static void read(String filePath) {
    try (InputStream inputStream = new FileInputStream(filePath)) {
      TGContext context = new TGContext();

      // Подключение плагинов для GP1-GP5
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
        sendChordsToServer(song);
      } else {
        System.err.println("Failed to read the song.");
      }
    } catch (Exception e) {
      System.err.println("Error processing file: " + e.getMessage());
    }
  }

  private static void sendChordsToServer(TGSong song) {
    Gson gson = new Gson();

    var trackIterator = song.getTracks();
    while (trackIterator.hasNext()) {
      TGTrack track = trackIterator.next();
      System.out.println("Processing track: " + track.getName());

      var measureIterator = track.getMeasures();
      while (measureIterator.hasNext()) {
        TGMeasure measure = measureIterator.next();

        for (TGBeat beat : measure.getBeats()) {
          if (beat.isChordBeat()) {
            TGChord tgChord = beat.getChord();

            JsonObject chordJson = new JsonObject();
            chordJson.addProperty("name", tgChord.getName());
            chordJson.addProperty("start_fret", tgChord.getFirstFret());
            chordJson.addProperty("barre", tgChord.getStrings() != null && tgChord.getStrings().length > 0 ? 1 : 0); // Простая логика для барре

            // Добавляем пальцы
            var fingersArray = gson.toJsonTree(createFingersJson(tgChord)).getAsJsonArray();
            chordJson.add("fingers", fingersArray);

            // Отправляем аккорд
            sendChordToServer(chordJson.toString());
          }
        }
      }
    }
  }

  private static JsonObject[] createFingersJson(TGChord chord) {
    int[] frets = chord.getStrings();
    JsonObject[] fingers = new JsonObject[frets.length];

    for (int i = 0; i < frets.length; i++) {
      JsonObject finger = new JsonObject();
      finger.addProperty("number", i + 1);
      finger.addProperty("fret", frets[i]);
      finger.addProperty("string", i + 1);
      fingers[i] = finger;
    }

    return fingers;
  }

  private static void sendChordToServer(String jsonChord) {
    try {
      URL url = new URL("http://localhost:5000/process-chord");
      HttpURLConnection connection = (HttpURLConnection) url.openConnection();
      connection.setRequestMethod("POST");
      connection.setRequestProperty("Content-Type", "application/json; utf-8");
      connection.setDoOutput(true);

      try (OutputStream os = connection.getOutputStream()) {
        byte[] input = jsonChord.getBytes("utf-8");
        os.write(input, 0, input.length);
      }

      int responseCode = connection.getResponseCode();
      System.out.println("Response Code: " + responseCode);

      if (responseCode == HttpURLConnection.HTTP_OK) {
        System.out.println("Chord successfully sent to Python.");
      } else {
        System.out.println("Failed to send chord. Response Code: " + responseCode);
      }

      connection.disconnect();
    } catch (Exception e) {
      System.err.println("Error sending chord to server: " + e.getMessage());
    }
  }
}
