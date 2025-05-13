from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Calendario F1 2025 (ejemplo, puedes actualizarlo con fechas reales)
races_2025 = [
    {"nombre": "Australian Grand Prix", "circuito": "Albert Park", "ubicacion": "Melbourne, Australia", "fecha": "2025-03-16", "hora": "05:00"},
    {"nombre": "Bahrain Grand Prix", "circuito": "Bahrain International Circuit", "ubicacion": "Sakhir, Bahrain", "fecha": "2025-03-23", "hora": "16:00"},
    {"nombre": "Chinese Grand Prix", "circuito": "Shanghai International Circuit", "ubicacion": "Shanghai, China", "fecha": "2025-04-06", "hora": "09:00"},
    {"nombre": "Emilia Romagna Grand Prix", "circuito": "Imola", "ubicacion": "Imola, Italia", "fecha": "2025-05-18", "hora": "15:00"},
    {"nombre": "Monaco Grand Prix", "circuito": "Circuit de Monaco", "ubicacion": "Monte Carlo, Monaco", "fecha": "2025-05-25", "hora": "15:00"},
    {"nombre": "Spanish Grand Prix", "circuito": "Circuit de Barcelona-Catalunya", "ubicacion": "Montmeló, España", "fecha": "2025-06-01", "hora": "15:00"},
    {"nombre": "Canadian Grand Prix", "circuito": "Circuit Gilles Villeneuve", "ubicacion": "Montreal, Canadá", "fecha": "2025-06-15", "hora": "20:00"},
    {"nombre": "Austrian Grand Prix", "circuito": "Red Bull Ring", "ubicacion": "Spielberg, Austria", "fecha": "2025-06-29", "hora": "15:00"},
    {"nombre": "British Grand Prix", "circuito": "Silverstone Circuit", "ubicacion": "Silverstone, Reino Unido", "fecha": "2025-07-06", "hora": "16:00"},
    {"nombre": "Hungarian Grand Prix", "circuito": "Hungaroring", "ubicacion": "Budapest, Hungría", "fecha": "2025-07-20", "hora": "15:00"},
    {"nombre": "Belgian Grand Prix", "circuito": "Circuit de Spa-Francorchamps", "ubicacion": "Spa, Bélgica", "fecha": "2025-07-27", "hora": "15:00"},
    {"nombre": "Dutch Grand Prix", "circuito": "Circuit Zandvoort", "ubicacion": "Zandvoort, Países Bajos", "fecha": "2025-08-24", "hora": "15:00"},
    {"nombre": "Italian Grand Prix", "circuito": "Autodromo Nazionale Monza", "ubicacion": "Monza, Italia", "fecha": "2025-08-31", "hora": "15:00"},
    {"nombre": "Azerbaijan Grand Prix", "circuito": "Baku City Circuit", "ubicacion": "Bakú, Azerbaiyán", "fecha": "2025-09-14", "hora": "13:00"},
    {"nombre": "Singapore Grand Prix", "circuito": "Marina Bay Street Circuit", "ubicacion": "Singapur", "fecha": "2025-09-21", "hora": "14:00"},
    {"nombre": "United States Grand Prix", "circuito": "Circuit of the Americas", "ubicacion": "Austin, Estados Unidos", "fecha": "2025-10-05", "hora": "21:00"},
    {"nombre": "Mexico City Grand Prix", "circuito": "Autódromo Hermanos Rodríguez", "ubicacion": "Ciudad de México, México", "fecha": "2025-10-26", "hora": "21:00"},
    {"nombre": "Brazilian Grand Prix", "circuito": "Interlagos", "ubicacion": "São Paulo, Brasil", "fecha": "2025-11-09", "hora": "18:00"},
    {"nombre": "Las Vegas Grand Prix", "circuito": "Las Vegas Street Circuit", "ubicacion": "Las Vegas, Estados Unidos", "fecha": "2025-11-22", "hora": "07:00"},
    {"nombre": "Qatar Grand Prix", "circuito": "Lusail International Circuit", "ubicacion": "Lusail, Qatar", "fecha": "2025-11-30", "hora": "16:00"},
    {"nombre": "Abu Dhabi Grand Prix", "circuito": "Yas Marina Circuit", "ubicacion": "Abu Dhabi, Emiratos Árabes Unidos", "fecha": "2025-12-07", "hora": "14:00"}
]

@app.route('/api/next_race')
def next_race():
    now = datetime.now()
    for race in races_2025:
        race_datetime = datetime.strptime(race["fecha"] + " " + race["hora"], "%Y-%m-%d %H:%M")
        if race_datetime > now:
            tiempo_restante = race_datetime - now
            dias = tiempo_restante.days
            horas, resto = divmod(tiempo_restante.seconds, 3600)
            minutos = resto // 60
            tiempo_str = f"{dias} días, {horas} horas, {minutos} minutos"
            return jsonify({
                "nombre": race["nombre"],
                "circuito": race["circuito"],
                "ubicacion": race["ubicacion"],
                "fecha": race["fecha"],
                "hora": race["hora"],
                "tiempo_restante": tiempo_str
            })
    return jsonify({"error": "No hay más carreras programadas para 2025."}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)
