from flask import Flask, jsonify, request
from flask_cors import CORS
from Conexion.ConexionDB import DBHelper
from metodosCRUD.usuarioCRUD import CRUDOperations

app = Flask(__name__)
CORS(app,  origins='http://localhost:3000')

# Configuración de la base de datos
db_helper = DBHelper(server='DESKTOP-KUMMTSM', database='Aurelia', trusted_connection=True)

crud_usuario = CRUDOperations(db_helper)

# Endpoint create_new_usuario
@app.route('/api/usuarios', methods=['POST'])
def create_new_usuario():
    try:
        # Obtener datos del cuerpo de la solicitud
        nombre = request.form['nombre']
        correo_electronico = request.form['correo_electronico']
        contrasena = request.form['contrasena']
        fecha_nacimiento = request.form['fecha_nacimiento']
        foto_perfil_data = request.files['foto_perfil'].read()  # Leer la imagen como bytes

        # Conectar a la base de datos
        db_helper.connect()

        # Crear un nuevo usuario
        result = crud_usuario.create_usuario(nombre, correo_electronico, contrasena, fecha_nacimiento, foto_perfil_data)

        # Devolver el resultado como respuesta
        return jsonify(result)

    except Exception as ex:
        # Manejar errores
        return jsonify({'error': str(ex)}), 500

    finally:
        # Cerrar la conexión
        db_helper.close()

# Endpoint para eliminar un usuario por ID
@app.route('/api/usuarios/<int:id_usuario>', methods=['DELETE'])
def delete_usuario(id_usuario):
    try:
        # Conectar a la base de datos
        db_helper.connect()

        # Eliminar el usuario por ID
        crud_usuario.delete_usuario(id_usuario)

        return jsonify({'message': 'Usuario eliminado correctamente'})

    except Exception as ex:
        # Manejar errores
        return jsonify({'error': str(ex)}), 500

    finally:
        # Cerrar la conexión
        db_helper.close()

# Endpoint para actualizar un usuario por ID
@app.route('/api/usuarios/<int:id_usuario>', methods=['PUT'])
def update_usuario(id_usuario):
    try:
        # Conectar a la base de datos
        db_helper.connect()

        # Obtener datos del cuerpo de la solicitud
        nombre = request.form['nombre']
        correo_electronico = request.form['correo_electronico']
        fecha_nacimiento = request.form['fecha_nacimiento']
        foto_perfil_data = request.files['foto_perfil'].read()  # Leer la nueva imagen como bytes
        contrasena = request.form['contrasena']

        # Actualizar el usuario
        result = crud_usuario.update_usuario(id_usuario, nombre, correo_electronico, fecha_nacimiento, foto_perfil_data, contrasena)

        return jsonify(result)

    except Exception as ex:
        # Manejar errores
        return jsonify({'error': str(ex)}), 500

    finally:
        # Cerrar la conexión
        db_helper.close()

# Endpoint para obtener todos los usuarios
@app.route('/api/usuarios', methods=['GET'])
def get_all_usuarios():
    try:
        # Conectar a la base de datos
        db_helper.connect()

        # Obtener todos los usuarios
        usuarios = crud_usuario.read_all_usuarios()

        # Devolver los usuarios como respuesta
        return jsonify(usuarios)

    except Exception as ex:
        # Manejar errores
        return jsonify({'error': str(ex)}), 500

    finally:
        # Cerrar la conexión
        db_helper.close()

if __name__ == '__main__':
    # Iniciar el servidor Flask
    app.run(debug=True)

    CORS(app)