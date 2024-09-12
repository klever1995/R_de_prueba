import pyodbc
import base64


class CRUDOperations:
    def __init__(self, db_helper):
        self.db_helper = db_helper

    # Crear un nuevo usuario
    def create_usuario(self, nombre, correo_electronico, contrasena, fecha_nacimiento, pais, materia_impartida,
                        foto_perfil_data):
        try:
            # Crear una instancia de cursor
            cursor = self.db_helper.connection.cursor()

            # Ejecutar la consulta para insertar un nuevo usuario con la imagen
            cursor.execute("""
                INSERT INTO Usuarios (nombre, correo_electronico, contrasena, fecha_nacimiento, foto_perfil)
                VALUES (?, ?, ?, ?, ?)
            """, nombre, correo_electronico, contrasena, fecha_nacimiento,
                               foto_perfil_data)

            # Confirmar la transacción
            self.db_helper.connection.commit()

            # Devolver un mensaje de éxito
            return {'message': 'Usuario creado exitosamente'}

        except pyodbc.Error as ex:
            print(f'Error de pyodbc: {ex}')
            raise

        finally:
            # Cerrar el cursor
            cursor.close()

    # eliminar usuarios
    def delete_usuario(self, id_usuario):
        try:
            cursor = self.db_helper.connection.cursor()

            # Eliminar usuario por ID
            cursor.execute("DELETE FROM Usuarios WHERE id_usuario = ?", id_usuario)

            # Confirmar la transacción
            self.db_helper.connection.commit()

        except pyodbc.Error as ex:
            print(f'Error de pyodbc: {ex}')
            raise

        finally:
            # Cerrar el cursor
            cursor.close()

    # Actualizar un usuario existente
    def update_usuario(self, id_usuario, nombre, correo_electronico, fecha_nacimiento,
                        foto_perfil_data, contrasena):
        try:
            # Crear una instancia de cursor
            cursor = self.db_helper.connection.cursor()

            # Ejecutar la consulta para actualizar el usuario
            cursor.execute("""
                UPDATE Usuarios
                SET nombre = ?, correo_electronico = ?, fecha_nacimiento = ?, foto_perfil = ?, contrasena = ?
                WHERE id_usuario = ?
            """, nombre, correo_electronico, fecha_nacimiento, foto_perfil_data,
                            contrasena,
                            id_usuario)

            # Confirmar la transacción
            self.db_helper.connection.commit()

            # Devolver un mensaje de éxito
            return {'message': 'Usuario actualizado exitosamente'}

        except pyodbc.Error as ex:
            print(f'Error de pyodbc: {ex}')
            raise

        finally:
            # Cerrar el cursor
            cursor.close()


    #Devolver todos los usuarios
    def read_all_usuarios(self):
        try:
            # Crear una instancia de cursor
            cursor = self.db_helper.connection.cursor()

            # Ejecutar la consulta para obtener todos los usuarios
            cursor.execute(
                "SELECT id_usuario, nombre, correo_electronico, fecha_nacimiento, foto_perfil FROM Usuarios")

            # Obtener todas las filas resultantes
            usuarios = cursor.fetchall()

            # Convertir las filas a un formato más adecuado
            result = []
            for row in usuarios:
                usuario = {
                    'id_usuario': row.id_usuario,
                    'nombre': row.nombre,
                    'correo_electronico': row.correo_electronico,
                    'fecha_nacimiento': row.fecha_nacimiento,
                }
                # Codificar la imagen de perfil a base64
                if row.foto_perfil:
                    encoded_image = base64.b64encode(row.foto_perfil).decode('utf-8')
                    usuario['foto_perfil'] = encoded_image
                else:
                    usuario['foto_perfil'] = None
                result.append(usuario)

            return result

        except pyodbc.Error as ex:
            print(f'Error de pyodbc: {ex}')
            raise

        finally:
            # Cerrar el cursor
            cursor.close()
