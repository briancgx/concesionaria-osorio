from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Crear instancia de Flask
app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://osorio:password@35.193.194.54/osorio'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar seguimiento de modificaciones
app.secret_key = 'supersecretkey'  # Necesario para usar flash messages
db = SQLAlchemy(app)

# Definición del modelo para la tabla Usuarios
class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    
    ID_Usuario = db.Column(db.Integer, primary_key=True)
    Nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)
    Contraseña = db.Column(db.String(100), nullable=False)
    Rol = db.Column(db.String(50), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Aquí puedes agregar lógica de autenticación
        return f"Bienvenido {username}!"
    return render_template("login.html")
# Ruta principal
@app.route('/')
def home():
    return render_template('index.html')  # Asegúrate de tener el archivo index.html en la carpeta templates/

@app.route('/panel')
def panel_control():
    return render_template('panel_control.html')
@app.route('/clientes')
def clientes():
    # Aquí puedes obtener la lista de clientes desde la base de datos
    return render_template('clientes.html')



if __name__ == '__main__':
    app.run(debug=True)
