
import base64
from flask import Blueprint, Flask, request, jsonify
from database import DatabaseConnection
from models.rooms_model import habitacionesModel

habitaciones_db = Blueprint('rooms_model', __name__)

@habitaciones_db.route('/', methods=['GET'])
def get_rooms():
    try:
        db = DatabaseConnection()  # Instancia de la clase Singleton
        query = "SELECT * FROM rooms"
        cursor = db.get_connection().cursor(dictionary=True)
        cursor.execute(query)
        rooms = cursor.fetchall()
        
        if rooms:
            for room in  rooms:
                if isinstance(room["image"],bytes):
                        room["image"] = base64.b64encode(room["image"]).decode('utf-8')
            return jsonify(rooms)
 # Devuelve un JSON con todas las habitaciones
        return jsonify({'message': 'No hay habitaciones registradas'}), 404
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return jsonify({'message': str(e)}), 500
    
@habitaciones_db.route('/rooms/<int:room_id>', methods=['GET'])
def get_room_by_id(room_id):
    """Endpoint para obtener una habitación por su ID."""
    room = habitacionesModel.get_id_rooms(room_id)
    
    if room:
        return jsonify(room), 200
    else:
        return jsonify({"error": "Habitación no encontrada"}), 404

@habitaciones_db.route('/', methods=['POST'])
def create_room():
    try:
            data = request.get_json()

            nombre = data['name_room']
            Tipo_de_habitacion = data['id_type_room']
            Piso = data['floor']
            Descripcion = data['description']
            imagen_bytes = data['image']
            Estado_de_la_habitacion = data['status_room']
            imagen_bytes= base64.b64decode(imagen_bytes)
            

            if not nombre or not isinstance (nombre,str):
                return jsonify({'message':'El nombre de la habitación es requerido y debe ser un string'}), 400
            if not Tipo_de_habitacion or not isinstance (Tipo_de_habitacion,int):
                return jsonify({'message':'El tipo de habitación es requerido y debe ser un entero'}), 400
            if not Piso or not isinstance (Piso,int):
                return jsonify({'message':'El piso es requerido y debe ser un entero'}), 400
            if not Estado_de_la_habitacion or not isinstance (Estado_de_la_habitacion,str):
                return jsonify({'message':'El estado de la habitación es requerido y debe ser un string'}), 400 
            
            if imagen_bytes:
                imagen_bytes = base64.b64decode(imagen_bytes)
            else:
                imagen_bytes = None  # Handle if there's no image

            print("Datos recividos en el backend", nombre, Tipo_de_habitacion, Piso, Descripcion, Estado_de_la_habitacion, imagen_bytes)
            
            rooms = habitacionesModel(nombre, Tipo_de_habitacion, Piso, Descripcion, Estado_de_la_habitacion,imagen_bytes)
            rooms.insert_room()


            return jsonify({"mensaje": "Habitación registrada correctamente"}), 200
    
        
    except Exception as e:
            print(f"Ocurrió un error: {e}")
            return jsonify({'message': str(e)}), 500


