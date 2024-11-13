# Realizar las importaciones de Flask
from flask import Flask, render_template, request
# from flask_mysqldb import MySQL

# Creación de un objeto-configuración
app = Flask(__name__)
# Conexión a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'prueba'

# Crear una instancia de la clase
# mysql = MySQL(app)

# Creación de las rutas --> URL
# HTTP Get, Post, Put, Delete
@app.route('/')
def home():
    return render_template('index.html')

# Recibir una petición Insomnia o Postman
@app.route('/add_contact', methods=['POST'])  # Cambiar method a methods
def add_contact():
    # Validación 
    if request.method == 'POST':
        # Cazar las variables
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        #Imprimir
        print(fullname)
        print(phone)
        print(email)
        return 'Recived'


# Ruta para Editar
@app.route('/edit')
def edit_contact():
    return '<h1>Actualizar contacto</h1>'

# Ruta para Eliminar
@app.route('/delete')
def delete_contact():
    return '<h1>Eliminar contacto</h1>'

if __name__ == '__main__':
    app.run(debug=True)
