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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Consultar la base de datos para verificar el usuario y la contraseña
        usuario = Usuario.query.filter_by(Nombre_usuario=username).first()

        # Si el usuario existe y la contraseña es correcta
        if usuario and usuario.Contraseña == password:
            # Redirigir al dashboard o página principal
            return redirect(url_for('dashboard'))
        else:
            # Si las credenciales son incorrectas, mostrar un mensaje de error
            flash('Credenciales incorrectas', 'error')
            return redirect(url_for('login'))
    
    # Si es GET, solo mostrar la página de login
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)
