from flask import Flask
from flask_cors import CORS
from microservicios.rooms_microservicio import habitaciones_db

app_rooms = Flask(__name__)

CORS(app_rooms)

# Registra el blueprint de habitaciones
app_rooms.register_blueprint(habitaciones_db, url_prefix='/rooms')

if __name__ == "__main__":
    print("🚀 Habitaciones Microservicio iniciado en http://localhost:5000")
    app_rooms.run(host='0.0.0.0', port=5000, debug=True)
    print("🚀 Habitaciones Microservicio iniciado en http://localhost:5000")