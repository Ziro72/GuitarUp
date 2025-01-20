from flask import Flask, request, jsonify
from Chord import Chord

app = Flask(__name__)

@app.route('/process-chord', methods=['POST'])
def process_chord():
    try:
        # Получение JSON с аккордом
        data = request.get_json()

        # Создание аккорда с помощью класса Chord
        chord = Chord(name=data['name'], fret=data['start_fret'])
        chord.edit_barre(data['barre'])

        # Добавляем пальцы в аккорд
        for finger in data['fingers']:
            chord.assign_finger(
                number=finger['number'] - 1,  # Номера пальцев начинаются с 0
                fret=finger['fret'],
                string=finger['string']
            )

        # Обновляем состояние струн
        chord.update_strings()

        # Отрисовываем аккорд и сохраняем
        chord.draw_chord()
        chord.save_chord()

        return jsonify({"status": "success", "message": f"Chord {data['name']} rendered successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)