from flask import Blueprint, Flask, request, jsonify
from flask_cors import CORS
import requests

api_gate=Flask(__name__)
CORS(api_gate, resources={r"/*": {"origins": "http://localhost:4200"}})

# Configuración de los microservicios
CHATBOT_SERVICE_URL = "http://localhost:5001/api"
HOTELLEXUS_SERVICE_URL = "http://localhost:5000"

@api_gate.route("/chatbot", methods=["POST"])
def chatbot():
    """Redirige la consulta al chatbot service y maneja errores correctamente."""
    data = request.get_json()
    print("🔍 Datos recibidos en API Gateway:", data)
    print(f"🔍 Enviando datos al chatbot en {CHATBOT_SERVICE_URL}/chatbot:", data) 

    if not data or "pregunta" not in data or "room_id" not in data:
        return jsonify({"error": "Faltan parámetros en la solicitud."}), 400

    try:
        response = requests.post(f"{CHATBOT_SERVICE_URL}/chatbot", json=data)
        print("✅ Respuesta del chatbot:", response.json())  # Depuración de respuesta

        # Manejo de respuesta vacía o fallida
        if response.status_code != 200 or not response.text.strip():
            return jsonify({"error": "No se obtuvo respuesta válida del chatbot."}), 500
        
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        print(f"❌ Error al comunicarse con el chatbot: {e}")
        return jsonify({"error": "No se pudo conectar con el chatbot."}), 500

@api_gate.route("/rooms", methods=["GET", "POST"])
def rooms():
    """Redirige la consulta al servicio de habitaciones."""
    try:
        if request.method == "GET":
            response = requests.get(f"{HOTELLEXUS_SERVICE_URL}/rooms")
        else:
            data = request.get_json()
            response = requests.post(f"{HOTELLEXUS_SERVICE_URL}/rooms", json=data)
        
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al comunicarse con el servicio de habitaciones: {e}")
        return jsonify({"error": "No se pudo conectar con el servicio de habitaciones."}), 500

if __name__ == "__main__":
    print("🚀 API Gateway iniciado en http://localhost:5002")
    api_gate.run(host='0.0.0.0', port=5002, debug=True)

