import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("⚠️ Error: La variable MONGO_URI no está definida en el archivo .env")

# Conectar a MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client["hotelLexus"]
clientes_collection = db["clientes"]  # Definiendo la colección

# Asegurar que 'clientes_collection' esté disponible para importar
__all__ = ["clientes_collection", "db"]
