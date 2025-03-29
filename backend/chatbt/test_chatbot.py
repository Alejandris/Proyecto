import requests

# URL del microservicio del chatbot
CHATBOT_URL = "http://localhost:5001/chatbot"

# Casos de prueba con preguntas y respuestas esperadas para los productos del 1 al 10
TEST_CASES = [
    {"room_id": 1, "pregunta": "¿Cuál es el procesador de este teléfono?", "esperado": "MediaTek Dimensity 8300-Ultra"},
    {"room_id": 1, "pregunta": "¿Cuánta RAM tiene este modelo?", "esperado": "12GB"},
    {"room_id": 1, "pregunta": "¿Cuál es el tamaño de la pantalla?", "esperado": "6.67 pulgadas"},
    {"room_id": 1, "pregunta": "¿Qué tipo de carga rápida soporta este smartphone?", "esperado": "67W"},
    {"room_id": 1, "pregunta": "¿Cuál es la capacidad de la batería?", "esperado": "5000mAh"},
    
    {"room_id": 2, "pregunta": "¿Qué procesador tiene este iPhone?", "esperado": "A16 Bionic"},
    {"room_id": 2, "pregunta": "¿Cuántos megapíxeles tiene la cámara principal?", "esperado": "48MP"},
    {"room_id": 2, "pregunta": "¿Es resistente al agua?", "esperado": "IP68"},
    {"room_id": 2, "pregunta": "¿Qué tamaño tiene la pantalla?", "esperado": "6.1 pulgadas"},
    {"room_id": 2, "pregunta": "¿Qué tecnología usa la pantalla?", "esperado": "Super Retina XDR"},
    
    {"room_id": 3, "pregunta": "¿Este modelo incluye un S-Pen?", "esperado": "Sí"},
    {"room_id": 3, "pregunta": "¿Cuál es la resolución de la pantalla?", "esperado": "QHD+"},
    {"room_id": 3, "pregunta": "¿Cuánta RAM tiene este modelo?", "esperado": "12GB"},
    {"room_id": 3, "pregunta": "¿Cuál es la tasa de refresco de la pantalla?", "esperado": "120Hz"},
    {"room_id": 3, "pregunta": "¿Qué procesador usa?", "esperado": "Snapdragon 8 Gen 2"},
    
    {"room_id": 4, "pregunta": "¿Qué versión de Android usa?", "esperado": "Android 13"},
    {"room_id": 4, "pregunta": "¿Cuántos megapíxeles tiene la cámara principal?", "esperado": "50MP"},
    {"room_id": 4, "pregunta": "¿Qué procesador tiene?", "esperado": "Google Tensor G2"},
    {"room_id": 4, "pregunta": "¿Qué tamaño tiene la pantalla?", "esperado": "6.7 pulgadas"},
    {"room_id": 4, "pregunta": "¿Cuál es la tasa de refresco de la pantalla?", "esperado": "120Hz"},
    
    {"room_id": 5, "pregunta": "¿Qué procesador tiene este teléfono?", "esperado": "Snapdragon 8 Gen 2"},
    {"room_id": 5, "pregunta": "¿Cuánta RAM tiene el OnePlus 11?", "esperado": "16GB"},
    {"room_id": 5, "pregunta": "¿Cuál es la velocidad de carga rápida?", "esperado": "100W"},
    {"room_id": 5, "pregunta": "¿Qué tamaño tiene la pantalla?", "esperado": "6.7 pulgadas"},
    {"room_id": 5, "pregunta": "¿Cuál es la resolución de la pantalla?", "esperado": "QHD+"},
    
    {"room_id": 6, "pregunta": "¿Cuántos megapíxeles tiene la cámara principal?", "esperado": "200MP"},
    {"room_id": 6, "pregunta": "¿Este modelo tiene carga inalámbrica?", "esperado": "Sí, 50W"},
    {"room_id": 6, "pregunta": "¿Qué procesador tiene?", "esperado": "Snapdragon 8+ Gen 1"},
    {"room_id": 6, "pregunta": "¿Cuál es la tasa de refresco de la pantalla?", "esperado": "144Hz"},
    {"room_id": 6, "pregunta": "¿Cuál es la velocidad de carga rápida?", "esperado": "125W"}
]

# Función para probar el chatbot
def probar_chatbot():
    total_preguntas = len(TEST_CASES)
    respuestas_correctas = 0
    
    for caso in TEST_CASES:
        payload = {"pregunta": caso["pregunta"], "room_id": caso["room_id"]}
        
        try:
            response = requests.post(CHATBOT_URL, json=payload)
            response_data = response.json()
            respuesta_chatbot = response_data.get("respuesta", "").strip().lower()
            esperado_lower = caso["esperado"].lower()
            
            # Considerar correcta la respuesta si contiene la respuesta esperada
            es_correcto = esperado_lower in respuesta_chatbot
            if es_correcto:
                respuestas_correctas += 1
            
            print(f"\n🔍 Probando Producto ID: {caso['room_id']}")
            print(f"✅ Pregunta: {caso['pregunta']}")
            print(f"   Esperado: {caso['esperado']}")
            print(f"   Respuesta Chatbot: {respuesta_chatbot}")
            print(f"   Resultado: {'✅ Correcto' if es_correcto else '❌ Incorrecto'}\n")
        except Exception as e:
            print(f"⚠️ Error al llamar al chatbot: {e}")
    
    # Calcular porcentaje de aciertos
    porcentaje_aciertos = (respuestas_correctas / total_preguntas) * 100
    print(f"\n📊 Estadísticas de prueba:")
    print(f"✅ Respuestas correctas: {respuestas_correctas} de {total_preguntas}")
    print(f"🎯 Precisión del chatbot: {porcentaje_aciertos:.2f}%")

# Ejecutar pruebas
if __name__ == "__main__":
    probar_chatbot()
