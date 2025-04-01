from datetime import date
import sys
sys.path.append("c:/Users/aleja/Proyectos/Proyecto_Final/backend")

from flask import Blueprint, request, jsonify
from flask_cors import CORS
from bson import ObjectId
from geolocaclizacion.dataMongo import clientes_collection

from geolocaclizacion.client_model import Cliente
from geolocaclizacion.dataMongo import db

cliente_bp = Blueprint("clientes", __name__)
CORS(cliente_bp)

@cliente_bp.route("/ubicationsadmin", methods=["POST"])
def crear_cliente():
    data = request.json
    cliente = Cliente(**data)
    resultado = clientes_collection.insert_one(cliente.to_dict())
    return jsonify({"mensaje": "Cliente creado", "id": str(resultado.inserted_id)})

@cliente_bp.route("/ubications", methods=["GET"])
def obtener_clientes():
    clientes = list(db.clientes.find())
    for cliente in clientes:
        cliente["_id"] = str(cliente["_id"])
    return jsonify(clientes)

@cliente_bp.route("/ubications/<id>", methods=["GET"])
def obtener_cliente(id):
    cliente = db.clientes.find_one({"_id": ObjectId(id)})
    if cliente:
        cliente["_id"] = str(cliente["_id"])
        return jsonify(cliente)
    return jsonify({"mensaje": "Cliente no encontrado"}), 404

@cliente_bp.route("/ubicationsadmin/<id>", methods=["PUT"])
def actualizar_cliente(id):
    data = request.json
    resultado = db.clientes.update_one({"_id": ObjectId(id)}, {"$set": data})
    if resultado.modified_count:
        return jsonify({"mensaje": "Cliente actualizado"})
    return jsonify({"mensaje": "Cliente no encontrado"}), 404

@cliente_bp.route("/ubicationsadmin/<id>", methods=["DELETE"])
def eliminar_cliente(id):
    resultado = db.clientes.delete_one({"_id": ObjectId(id)})
    if resultado.deleted_count:
        return jsonify({"mensaje": "Cliente eliminado"})
    return jsonify({"mensaje": "Cliente no encontrado"}), 404
    