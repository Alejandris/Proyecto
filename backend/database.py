from mysql.connector import Error
import mysql.connector

class DatabaseConnection:
    """Clase Singleton para manejar la conexión a MySQL."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            try:
                # Intentar establecer la conexión
                cls._instance.connection = mysql.connector.connect(
                    host="localhost",
                    port=3306,
                    user="root",
                    password="123456",
                    database="hotellexus"
                )
                # Verificar si la conexión fue exitosa
                if cls._instance.connection.is_connected():
                    print("Conexión exitosa a la base de datos")
                else:
                    raise Error("No se pudo conectar a la base de datos")
            except Error as e:
                print(f"Error al conectar a la base de datos: {e}")
                cls._instance.connection = None  # Asegurarse de que no haya una conexión errónea
        return cls._instance

    def get_connection(self):
        """Devuelve la conexión a la base de datos."""
        if self.connection is None:
            print("No hay una conexión válida.")
        return self.connection


    def create_connection():
        try:
            # Intentamos establecer la conexión
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='123456',
                database='hotellexus'
            )

            # Verificamos si la conexión se ha establecido correctamente
            if connection.is_connected():
                print("Conexión exitosa a la base de datos")
            else:
                print("No se pudo establecer la conexión")
                return None  # Si la conexión falla, devolvemos None

            return connection  # Si la conexión es exitosa, devolvemos el objeto de conexión

        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            return None  # Devolvemos None si ocurre algún error

    # Usamos la función para obtener la conexión
    connection = create_connection()

    if connection:
        # Si la conexión es válida, usamos el cursor
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM rooms")  # Ejecutar una consulta
        result = cursor.fetchall()
        print(result)
        cursor.close()
        connection.close()
    else:
        print("No se pudo establecer la conexión, no se puede ejecutar la consulta.")
