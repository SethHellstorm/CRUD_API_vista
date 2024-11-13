from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector # type: ignore

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Configuración de la conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',  
        password='',  
        database='ricarte'
    )

# Rutas de la API
@app.route('/alumnos', methods=['GET'])
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

@app.route('/alumnos/<int:id_alum>', methods=['GET'])
def get_alumno(id_alum):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM alumnos WHERE id = %s', (id_alum,))
        alumno = cursor.fetchone()
        if alumno:
            return jsonify(alumno)
        return jsonify({"error": "Alumno no encontrado"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@app.route('/alumnos', methods=['POST'])
def add_alumno():
    try:
        new_alumno = request.get_json()
        required_fields = ['name', 'carrera', 'edad']
        
        # Validar campos requeridos
        for field in required_fields:
            if field not in new_alumno:
                return jsonify({"error": f"Falta el campo {field}"}), 400

        connection = get_db_connection()
        cursor = connection.cursor()
        
        query = 'INSERT INTO alumnos (name, carrera, edad) VALUES (%s, %s, %s)'
        values = (new_alumno['name'], new_alumno['carrera'], new_alumno['edad'])
        
        cursor.execute(query, values)
        connection.commit()
        
        return jsonify({"message": "Alumno creado exitosamente", "id": cursor.lastrowid}), 201
    
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@app.route('/alumnos/<int:id_item>', methods=['PUT'])
def update_alumno(id_item):
    try:
        dato = request.get_json()
        required_fields = ['name', 'carrera', 'edad']
        
        # Validar campos requeridos
        for field in required_fields:
            if field not in dato:
                return jsonify({"error": f"Falta el campo {field}"}), 400

        connection = get_db_connection()
        cursor = connection.cursor()
        
        query = 'UPDATE alumnos SET name = %s, carrera = %s, edad = %s WHERE id = %s'
        values = (dato['name'], dato['carrera'], dato['edad'], id_item)
        
        cursor.execute(query, values)
        connection.commit()
        
        if cursor.rowcount > 0:
            return jsonify({"message": "Alumno actualizado exitosamente"})
        return jsonify({"error": "Alumno no encontrado"}), 404
    
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@app.route('/alumnos/<int:id_item>', methods=['DELETE'])
def delete_alumno(id_item):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute('DELETE FROM alumnos WHERE id = %s', (id_item,))
        connection.commit()
        
        if cursor.rowcount > 0:
            return jsonify({"message": "Alumno eliminado exitosamente"})
        return jsonify({"error": "Alumno no encontrado"}), 404
    
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# Manejador de errores para rutas no encontradas
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ruta no encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)