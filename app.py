from flask import Flask, render_template, request, redirect, url_for, flash
from routes.main import main_bp
from models import db, Usuario, Cliente, Credito, Vehiculo, Compra, Inventario, AtencionAlCliente, HistorialCredito, Pago, Reporte

# Crear instancia de Flask
app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@40.76.251.76/osorio'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar seguimiento de modificaciones
app.secret_key = 'supersecretkey'  # Necesario para usar flash messages

# Inicializar SQLAlchemy con la aplicación
db.init_app(app)

# Registrar el blueprint
app.register_blueprint(main_bp)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('login.html')  # Mostrar el formulario directamente

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre_usuario = request.form['username']
        contrasena = request.form['password']
        
        usuario = Usuario.query.filter_by(Nombre_usuario=nombre_usuario).first()
        
        if usuario and usuario.Contraseña == contrasena:
            flash('¡Inicio de sesión exitoso!', 'success')
            #return redirect(url_for('main.panel_control'))
                        # Redirigir según el rol del usuario
            if usuario.Rol == 'Administrador':
                return redirect(url_for('main.panel_control'))  # Redirige al panel del administrador
            elif usuario.Rol == 'Gerente':
                return redirect(url_for('main.panel_gerente'))  # Redirige al panel del gerente
            elif usuario.Rol == 'Asesor Ventas':
                return redirect(url_for('main.panel_asesor'))  # Redirige al panel del asesor de ventas
            elif usuario.Rol == 'Asistente':
                return redirect(url_for('main.panel_asistente'))  # Redirige al panel del asistente administrativo
            else:
                flash('Rol no reconocido', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Credenciales incorrectas. Intenta de nuevo.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
