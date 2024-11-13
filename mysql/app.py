from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
 
app = Flask(__name__)
 
def get_db_connection(): #Conexion a la base de datos
    return mysql.connector.connect(
        host='localhost',
        user='root',  
        password='654321Test',  
        database='pruebaconexion'  
    )
 
@app.route('/alumnos', methods=['GET']) #Mostrar toda la informacion de la tabla
def get_alumnos():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM alumnos')  
        alumnos = cursor.fetchall()
        return jsonify(alumnos)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
 
@app.route('/alumnos/<int:id_alum>', methods=['GET']) #Buscar la info de un alumno con su id
def get_alumno(id_alum):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM alumnos WHERE id = %s', (id_alum,))
    item = cursor.fetchone()
    cursor.close()
    connection.close()

    if item: #Si existe el alumno
        return jsonify(item)
    else: #Si no existe el alumno
        return jsonify({'Error': 'No se encontro al alumno'}), 404
 
@app.route('/alumnos', methods=['POST']) #Añadir un alumno a la tabla
def create_alumno():
    new_item = request.json
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO alumnos (nombre, edad, carrera) VALUES (%s, %s, %s)', 
                   (new_item['nombre'], new_item['edad'], new_item['carrera']))  #Inserta en la tabla, deben de ser todos los campos de fila
    connection.commit()
    cursor.close()
    connection.close()    
    return jsonify({'message': 'Alumno añadido exitosamente'}), 201

@app.route('/alumnos/<int:id_item>', methods=['PUT']) #Actualizar un alumno de la tabla
def update_alumno(id_item):
    updated_item = request.json
    connection = get_db_connection()
    cursor = connection.cursor()

    # Verificar si existe el alumno
    cursor.execute('SELECT * FROM alumnos WHERE id = %s', (id_item,))
    existing_item = cursor.fetchone()

    if existing_item: # Actualizar el alumno si existe       
        cursor.execute('UPDATE alumnos SET nombre = %s, edad = %s, carrera = %s WHERE id = %s',
                       (updated_item['nombre'], updated_item['edad'], updated_item['carrera'], id_item))  
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Alumno actualizado correctamente'})
    else:
        #Mensaje si el alumno no existe
        cursor.close()
        connection.close()
        return jsonify({'Error': 'Alumno no existe'}), 404


#Crear ruta para eliminar 
@app.route('/alumnos/<int:id_item>', methods=['DELETE'])
def delete_alumno(id_item):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Verificar si el alumno existe
    cursor.execute('SELECT * FROM alumnos WHERE id = %s', (id_item,))
    existing_item = cursor.fetchone()

    if existing_item:
        # Eliminar el alumno
        cursor.execute('DELETE FROM alumnos WHERE id = %s', (id_item,))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Alumno eliminado'})
    else:
        cursor.close()
        connection.close()
        return jsonify({'Error': 'Alumno no existe'}), 404
 
if __name__ == '__main__':
    app.run(debug=True)