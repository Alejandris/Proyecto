from flask import Blueprint, Flask, request, jsonify
from flask_cors import CORS
import requests

api_gateway = Blueprint("api_gateway", __name__)
CORS(api_gateway)

# Configuración de los microservicios
CHATBOT_SERVICE_URL = "http://localhost:5001"
HOTELLEXUS_SERVICE_URL = "http://localhost:5000"

@api_gateway.route("/chatbot", methods=["POST"])
def chatbot():
    """Redirige la consulta al chatbot service y maneja errores correctamente."""
    data = request.get_json()

    if not data or "pregunta" not in data or "room_id" not in data:
        return jsonify({"error": "Faltan parámetros en la solicitud."}), 400

    try:
        response = requests.post(f"{CHATBOT_SERVICE_URL}/chat", json=data)

        # Manejo de respuesta vacía o fallida
        if response.status_code != 200 or not response.text.strip():
            return jsonify({"error": "No se obtuvo respuesta válida del chatbot."}), 500
        
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        print(f"❌ Error al comunicarse con el chatbot: {e}")
        return jsonify({"error": "No se pudo conectar con el chatbot."}), 500

@api_gateway.route("/rooms", methods=["GET", "POST"])
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

