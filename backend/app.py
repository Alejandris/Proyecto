from flask import Flask
from flask_cors import CORS
from microservicios.rooms_microservicio import habitaciones_db
from microservicios.MicroServicioWebScraping import scrape

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})
# Habilita CORS en los Blueprints
CORS(habitaciones_db)
CORS(scrape)
# Registra el blueprint de habitaciones
app.register_blueprint(habitaciones_db, url_prefix='/rooms')
app.register_blueprint(scrape, url_prefix='/api')

if __name__ == "__main__":
    print("🚀 Habitaciones Microservicio iniciado en http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)