from flask import Flask, request, jsonify
from Chord import Chord
import traceback

app = Flask(__name__)

@app.route('/process-chord', methods=['POST'])
def process_chord():
    try:
        # Получение JSON с аккордом
        data = request.get_json()
        if not data:
            app.logger.error("No JSON data provided.")
            return jsonify({"status": "error", "message": "No JSON data provided."}), 400

        app.logger.info(f"Received chord data: {data}")

        # Создание аккорда с помощью класса Chord
        chord = Chord(name=data.get('name', ""), fret=data.get('start_fret', 0))
        chord.edit_barre(data.get('barre', 0))

        # Добавляем пальцы в аккорд
        fingers = data.get('fingers', [])
        for finger in fingers:
            chord.assign_finger(
                number=finger.get('number', 0) - 1,  # Номера пальцев начинаются с 0
                fret=finger.get('fret', 0),
                string=finger.get('string', 0)
            )

        app.logger.info("Assigned fingers to chord.")

        # Обновляем состояние струн
        chord.update_strings()

        # Отрисовываем аккорд и сохраняем
        chord.draw_chord()
        chord.save_chord()

        app.logger.info(f"Chord {data.get('name', '')} rendered successfully.")

        return jsonify({"status": "success", "message": f"Chord {data.get('name', '')} rendered successfully."})
    except Exception as e:
        # Логируем стек вызовов для отладки
        traceback_str = traceback.format_exc()
        app.logger.error(f"Error processing chord: {str(e)}\n{traceback_str}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
