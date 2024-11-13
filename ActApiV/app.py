from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
 
from flask_cors import CORS  # Agrega esta importación

app = Flask(__name__)
CORS(app)  # Habilita CORS en la aplicación
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '654321Test'
app.config['MYSQL_DB'] = 'pruebaconexion'

mysql = MySQL(app)
 
@app.route('/alumnos', methods=['GET']) #Mostrar toda la informacion de la tabla
def get_items():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM alumnos")
    rows = cursor.fetchall()
    items = [{"id": row[0], "name": row[1], "edad": row[2], "carrera": row[3]} for row in rows]
    return jsonify(items)
 
@app.route('/alumnos', methods=['POST']) #Añadir un alumno a la tabla
def create_alumno():
    data = request.get_json()
    name = data.get('name')
    edad = data.get('edad')
    carrera = data.get('carrera')
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO alumnos (nombre, edad, carrera) VALUES (%s, %s, %s)", (name, edad, carrera))
    mysql.connection.commit()
    return jsonify({"message": "Alumno añadido"}), 201


@app.route('/alumnos/<int:id_item>', methods=['PUT']) #Actualizar un alumno de la tabla
def update_item(id_item):
    data = request.get_json()
    name = data.get('name')
    edad = data.get('edad')
    carrera = data.get('carrera')
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE alumnos SET nombre = %s, edad = %s, carrera = %s WHERE id = %s", (name, edad, carrera, id_item))
    mysql.connection.commit()
    return jsonify({"message": "Alumno actualizado"}), 200

#Crear ruta para eliminar 
@app.route('/alumnos/<int:id_item>', methods=['DELETE'])
def delete_alumno(id_item):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM alumnos WHERE id = %s", (id_item,))
    mysql.connection.commit()
    return jsonify({"message": "Alumno eliminado"}), 200
        
 
if __name__ == '__main__':
    app.run(debug=True)