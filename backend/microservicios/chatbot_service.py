from flask import  Blueprint, Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

from models.rooms_model import habitacionesModel



chatbotc =Blueprint('chatbotc', __name__)
CORS(chatbotc)
# Cargar modelo de QA
#print("🚀 Iniciando carga de modelos...")

#qa_pipeline = pipeline("question-answering",model="mrm8488/bert-spanish-cased-finetuned-squad-es")

#qa_pipeline = pipeline("question-answering", model="mrm8488/electra-small-spanish-squad2")


qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad",max_answer_length=50)


print("✅ Modelo de QA cargado.")

def obtener_contexto(room_id):
    """Obtiene la descripción de la habitación desde la base de datos."""
    print(f"🔍 Buscando contexto para habitación ID: {room_id}")

    try:
        room = habitacionesModel.get_id_rooms(room_id)  # Asegúrate de que devuelve datos
        print(f"📌 Datos obtenidos de la BD: {room}")  

        if not room or not room.get('description'):
            print("❌ Error: La habitación no tiene descripción válida.")
            return "Descripción no encontrada."

        return room['description']
    except Exception as e:
        print(f"❌ Error al obtener datos de la BD: {e}")
        return "Error al obtener la información de la habitación."

@chatbotc.route("/chatbot", methods=["POST"])
def chatbot():
    """Procesa la pregunta del usuario con el contexto del habitacion."""
    datos = request.get_json()
    print("Datos recibidos en el servidor:", datos)
    pregunta = datos.get("pregunta", "")
    room_id = datos.get("room_id", "")
    print(datos)
    
    if not room_id:
        return jsonify({"error": "Falta el ID del habitacion."}), 400
    
    contexto = obtener_contexto(room_id)
    
    if contexto == "Descripción no encontrada.":
        return jsonify({"error": "No se encontró información sobre este habitacion."}), 404
    
    respuesta = qa_pipeline({"question": pregunta, "context": contexto})
    return jsonify({"respuesta": respuesta["answer"]})
