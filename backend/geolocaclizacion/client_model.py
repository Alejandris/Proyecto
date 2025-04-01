import base64
import requests

class Cliente:
    def __init__(self, razonSocial, direccion, ubicacion=None, imagenBase64=None, sedes=None):
        self.razonSocial = razonSocial
        self.direccion = direccion
        # Ubicación puede ser manual ([latitud, longitud]) o obtenida con Mapbox
        self.ubicacion = ubicacion if ubicacion else []
        self.imagenBase64 = imagenBase64

    def to_dict(self):
        return {
            "razonSocial": self.razonSocial,
            "direccion": self.direccion,
            "ubicacion": self.ubicacion,
            "imagenBase64": self.imagenBase64
        }

    @staticmethod
    def encode_image(image_path):
        """Codifica una imagen a formato Base64."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    @staticmethod
    def decode_image(base64_string, output_path):
        """Decodifica una imagen desde Base64 y la guarda en disco."""
        with open(output_path, "wb") as image_file:
            image_file.write(base64.b64decode(base64_string))

    @staticmethod
    def get_coordinates(address, mapbox_token):
        """Obtiene coordenadas usando la API de Mapbox."""
        MAPBOX_TOKEN = "pk.eyJ1IjoiYWxlamFuZHJpcyIsImEiOiJjbThwemdzenMwZ2M0MmxxMnM4bHB1MnFpIn0.ZZ7Rh1LYjb-KT7OpCvSjNA"
        address = address.replace("Bogota, Colombia")
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json?access_token={MAPBOX_TOKEN}"
        response = requests.get(url)
        data = response.json()
        if "features" in data and len(data["features"]) > 0:
            coords = data["features"][0]["geometry"]["coordinates"]
            return [coords[1], coords[0]]  # Retorna [latitud, longitud]
        return None
