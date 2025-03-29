# from flask import Blueprint, Flask, request, jsonify
# from backend.models.rooms_model import habitacionesModel
# import spacy
# from gensim.models import KeyedVectors
# from transformers import pipeline

# chatbot_service_old = Blueprint('chatbot_service_old', __name__)

# # Cargar modelos NLP
# print("🚀 Iniciando carga de modelos...")
# nlp = spacy.load("es_core_news_md")
# print("✅ spaCy es_core_news_md cargado.")

# qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
# print("✅ Modelo de QA cargado.")

# try:
#     print("✅ Cargando FastText")
#     modelo_fasttext = KeyedVectors.load_word2vec_format("cc.es.300.vec.gz", binary=False)
#     print("✅ FastText cargado.")
# except Exception as e:
#     print(f"⚠️ Error al cargar FastText: {e}")
#     modelo_fasttext = None

# def extraer_sustantivos(pregunta):
#     """Extrae sustantivos de la pregunta usando spaCy."""
#     doc = nlp(pregunta)
#     return [token.text for token in doc if token.pos_ == "NOUN"]

# def expandir_pregunta(sustantivos):
#     """Expande la pregunta buscando palabras relacionadas con FastText."""
#     palabras_expandidas = []
#     if modelo_fasttext:
#         for sustantivo in sustantivos:
#             similares = modelo_fasttext.most_similar(sustantivo, topn=3)
#             palabras_expandidas.extend([palabra[0] for palabra in similares])
#     return palabras_expandidas

# def obtener_contexto():
#     """Obtiene el contexto de habitaciones (nombre y descripción)."""
#     room = habitacionesModel.get_id_rooms()
#     contexto = " ".join([f"{r['name']}: {r['description']}" for r in room])
#     return contexto

# @chatbot_service_old.route("/chat", methods=["POST"])
# def chat():
#     """Procesa la pregunta del usuario, expandiéndola si es posible."""
#     datos = request.get_json()
#     pregunta = datos.get("pregunta", "")
    
#     # Extraer sustantivos y expandir pregunta
#     sustantivos = extraer_sustantivos(pregunta)
#     palabras_expandidas = expandir_pregunta(sustantivos)
    
#     # Obtener contexto de la base de datos
#     contexto = obtener_contexto()
    
#     respuesta = qa_pipeline({"question": pregunta, "context": contexto})
#     return jsonify({"respuesta": respuesta["answer"], "expansion": palabras_expandidas})

