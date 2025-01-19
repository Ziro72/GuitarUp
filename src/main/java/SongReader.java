import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import org.herac.tuxguitar.io.base.TGFileFormatManager;
import org.herac.tuxguitar.io.base.TGSongReaderHandle;
import org.herac.tuxguitar.song.factory.TGFactory;
import org.herac.tuxguitar.song.models.*;

import java.io.FileInputStream;
import java.io.InputStream;

public class SongReader {

    public static void read(String filePath) {
        try (InputStream inputStream = new FileInputStream(filePath)) {
            TGContext context = new TGContext();

            // Подключение плагинов для GP1-GP5 и GPX
            new GP1InputStreamPlugin().connect(context);
            new GP2InputStreamPlugin().connect(context);
            new GP3InputStreamPlugin().connect(context);
            new GP4InputStreamPlugin().connect(context);
            new GP5InputStreamPlugin().connect(context);
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
                extractChordsFromSong(song);
            } else {
                System.err.println("Failed to read the song.");
            }
        } catch (Exception e) {
            System.err.println("Error processing file: " + e.getMessage());
        }
    }

    private static void extractChordsFromSong(TGSong song) {
        var trackIterator = song.getTracks();
        while (trackIterator.hasNext()) {
            TGTrack track = trackIterator.next();
            var measureIterator = track.getMeasures();
            while (measureIterator.hasNext()) {
                TGMeasure measure = measureIterator.next();
                for (TGBeat beat : measure.getBeats()) {
                    if (beat.isChordBeat()) {
                        TGChord chord = beat.getChord();
                        String json = convertChordToJson(chord);
                        ChordSender.sendChord(json);
                    }
                }
            }
        }
    }

    private static String convertChordToJson(TGChord chord) {
        JsonObject jsonObject = new JsonObject();
        jsonObject.addProperty("name", chord.getName());
        jsonObject.addProperty("start_fret", chord.getFirstFret());
        jsonObject.addProperty("barre", chord.getBarre()); // Убедитесь, что Barre корректно реализован

        JsonArray fingers = new JsonArray();
        for (int i = 0; i < chord.countFingers(); i++) {
            JsonObject fingerJson = new JsonObject();
            TGChord.Finger finger = chord.getFinger(i); // Добавьте метод для получения пальца
            fingerJson.addProperty("number", i + 1);
            fingerJson.addProperty("fret", finger.getFret());
            fingerJson.addProperty("string", finger.getString());
            fingers.add(fingerJson);
        }
        jsonObject.add("fingers", fingers);

        return jsonObject.toString();
    }
}
