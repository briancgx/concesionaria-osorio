from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from routes.main import main_bp

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
def home():
    return render_template('login.html')  # Mostrar el formulario directamente

# Ruta para el login (GET y POST)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre_usuario = request.form['username']
        contrasena = request.form['password']
        
        # Buscar el usuario en la base de datos
        usuario = Usuario.query.filter_by(Nombre_usuario=nombre_usuario).first()
        
        if usuario and usuario.Contraseña == contrasena:
            # Si las credenciales son correctas
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('dashboard'))  # Redirige al dashboard o página de inicio
        else:
            # Si las credenciales son incorrectas
            flash('Credenciales incorrectas. Intenta de nuevo.', 'error')
            return redirect(url_for('login'))  # Vuelve al formulario de login

    return render_template('login.html')  # Renderiza el formulario de login

# Ruta para el dashboard (puedes personalizarla según tus necesidades)
@app.route('/dashboard')
def dashboard():
    return '¡Bienvenido al Dashboard!'

app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
