from flask import Flask
from flask_cors import CORS
from microservicios.chatbot_service import chatbotc

app_chat = Flask(__name__)

CORS(app_chat, resources={r"/*": {"origins": "http://localhost:4200"}})

# Registra los blueprints

app_chat.register_blueprint(chatbotc, url_prefix='/api')

if __name__ == "__main__":
    print("🚀 Chatbot y API Gateway iniciado en http://localhost:5001")
    app_chat.run(host='0.0.0.0', port=5001, debug=True)
