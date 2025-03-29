from database import DatabaseConnection


class habitacionesModel:
    def __init__(self,  name_room, id_type_room, floor, description, status_room, image = None):
        self.name_room = name_room
        self.id_type_room = id_type_room
        self.floor = floor
        self.description = description
        self.status_room = status_room
        self.image = image

    @classmethod
    def get_all_rooms(cls):
            """Obtiene todas las habitaciones de la base de datos."""
            query = "SELECT * FROM rooms"
            cursor = DatabaseConnection().get_connection().cursor()
            cursor.execute(query)
            rooms = cursor.fetchall()
            cursor.close()
            return rooms
    
    @classmethod
    def get_id_rooms(room_id):
            """Obtiene un habitacion específico por su ID."""
            try:
                conexion = DatabaseConnection().get_connection()
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("SELECT * FROM rooms WHERE id = %s;", (room_id,))
                rooms = cursor.fetchone()
                return rooms
            except Exception as e:
                print(f"❌ Error al obtener habitacion por ID: {e}")
                return None
        
    def insert_room(self):
            """Inserta una nueva habitación en la base de datos."""
            try:
                query = """
                    INSERT INTO rooms (name_room, id_type_room, floor, description, status_room, image)
                    VALUES (%s, %s, %s, %s, %s,%s)
                """
                cursor = DatabaseConnection().get_connection().cursor()
                cursor.execute(query, (self.name_room, self.id_type_room, self.floor, self.description, self.status_room, self.image))
                
                # Confirmar la transacción
                DatabaseConnection().get_connection().commit()
                print(f"Habitación {self.name_room} insertada correctamente.")
                
                cursor.close()
            except Exception as e:
                print(f"Error al insertar habitación: {e}")
                DatabaseConnection().get_connection().rollback()  # En caso de error, revertir la transacción
                cursor.close()