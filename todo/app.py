from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import logging

app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir el acceso desde el frontend

# Configuración de la conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="Josejovel102030",  
    port="3306",
    database="db_academica"
)


logging.basicConfig(level=logging.DEBUG)

@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    try:
        data = request.get_json()
        logging.debug("Datos recibidos: %s", data)  # Verificar qué datos llegan
        if not data:
            return jsonify({"message": "No se recibieron datos"}), 400
        
        cursor = db.cursor()
        sql = "INSERT INTO usuarios (usuario, clave, nombre, direccion, telefono) VALUES (%s, %s, %s, %s, %s)"
        val = (data['usuario'], data['clave'], data['nombre'], data['direccion'], data['telefono'])
        logging.debug("Ejecutando SQL: %s con valores %s", sql, val)
        cursor.execute(sql, val)
        db.commit()
        
        logging.info("Registro exitoso")
        return jsonify({"message": "Usuario registrado exitosamente"}), 201
    except Exception as e:
        logging.error("Error al registrar usuario: %s", e)
        return jsonify({"message": f"Error al registrar usuario: {str(e)}"}), 400
    finally:
        cursor.close()

@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        return jsonify(usuarios)
    except Exception as e:
        logging.error("Error al obtener usuarios: %s", e)
        return jsonify({"message": f"Error al obtener usuarios: {str(e)}"}), 400
    finally:
        cursor.close()

@app.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    try:
        data = request.get_json()
        logging.debug("Datos recibidos para actualizar: %s", data)
        cursor = db.cursor()
        sql = "UPDATE usuarios SET usuario=%s, clave=%s, nombre=%s, direccion=%s, telefono=%s WHERE idUsuario=%s"
        val = (data['usuario'], data['clave'], data['nombre'], data['direccion'], data['telefono'], id)
        logging.debug("Ejecutando SQL: %s con valores %s", sql, val)
        cursor.execute(sql, val)
        db.commit()
        return jsonify({"message": "Usuario actualizado exitosamente"})
    except Exception as e:
        logging.error("Error al actualizar usuario: %s", e)
        return jsonify({"message": f"Error al actualizar usuario: {str(e)}"}), 400
    finally:
        cursor.close()

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    try:
        cursor = db.cursor()
        sql = "DELETE FROM usuarios WHERE idUsuario=%s"
        logging.debug("Ejecutando SQL: %s con id %s", sql, id)
        cursor.execute(sql, (id,))
        db.commit()
        return jsonify({"message": "Usuario eliminado exitosamente"})
    except Exception as e:
        logging.error("Error al eliminar usuario: %s", e)
        return jsonify({"message": f"Error al eliminar usuario: {str(e)}"}), 400
    finally:
        cursor.close()

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        logging.debug("Intento de login con datos: %s", data)
        cursor = db.cursor(dictionary=True)
        sql = "SELECT * FROM usuarios WHERE usuario=%s AND clave=%s"
        cursor.execute(sql, (data['usuario'], data['clave']))
        usuario = cursor.fetchone()
        if usuario:
            return jsonify({"autorizado": True})
        else:
            return jsonify({"autorizado": False})
    except Exception as e:
        logging.error("Error en login: %s", e)
        return jsonify({"message": f"Error en login: {str(e)}"}), 400
    finally:
        cursor.close()

if __name__ == '__main__':
    app.run(port=5000, debug=True)

