from flask import Flask, jsonify
import requests
from flask_cors import CORS  # <--- Agrega esto

app = Flask(__name__)
CORS(app)  # <--- Y esto

# ...resto del código...

ERGAST_API_URL = "https://ergast.com/api/f1/current/driverStandings.json"

@app.route("/api/campeonato", methods=["GET"])
def campeonato():
    response = requests.get(ERGAST_API_URL)
    if response.status_code != 200:
        return jsonify({"error": "No se pudo obtener la información"}), 500
    data = response.json()
    standings_list = data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
    tabla = []
    for piloto in standings_list:
        driver = piloto["Driver"]
        constructor = piloto["Constructors"][0]
        tabla.append({
            "posicion": piloto["position"],
            "puntos": piloto["points"],
            "victorias": piloto["wins"],
            "nombre": f"{driver['givenName']} {driver['familyName']}",
            "nacionalidad": driver["nationality"],
            "equipo": constructor["name"]
        })
    return jsonify(tabla)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
