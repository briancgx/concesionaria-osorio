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



# Definición del modelo para la tabla Clientes
class Cliente(db.Model):
       __tablename__ = 'Clientes'
       
       ID_Cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
       Nombre = db.Column(db.String(50), nullable=False)
       Dirección = db.Column(db.String(100), nullable=True)
       Teléfono = db.Column(db.String(10), nullable=True)
       Correo_electrónico = db.Column(db.String(50), nullable=True)
       Estado_cliente = db.Column(db.String(10), nullable=True)
def __repr__(self):
        return f'<Cliente {self.Nombre}>'
class Credito(db.Model):
    __tablename__ = 'Créditos'
    
    ID_Credito = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ID_Cliente = db.Column(db.Integer, db.ForeignKey('Clientes.ID_Cliente'), nullable=False)
    Monto_crédito = db.Column(db.Numeric(10, 2), nullable=True)
    Interés = db.Column(db.Numeric(4, 2), nullable=True)
    Fecha_otorgamiento = db.Column(db.Date, nullable=True)
    Estado_Crédito = db.Column(db.String(10), nullable=True)

    # Relación con el modelo Cliente
    cliente = db.relationship('Cliente', backref='creditos')

class Vehiculo(db.Model):
    __tablename__ = 'Vehículos'
    
    ID_Vehículo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ID_Cliente = db.Column(db.Integer, db.ForeignKey('Clientes.ID_Cliente'), nullable=True)  # Clave foránea opcional
    Marca = db.Column(db.String(50), nullable=True)
    Modelo = db.Column(db.String(50), nullable=True)
    Año = db.Column(db.Integer, nullable=True)
    Tipo = db.Column(db.String(30), nullable=True)

    # Relación con el modelo Cliente (opcional)
    cliente = db.relationship('Cliente', backref='vehículos')

class Compra(db.Model):
    __tablename__ = 'Compra'
    
    ID_Compra = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ID_Cliente = db.Column(db.Integer, db.ForeignKey('Clientes.ID_Cliente'), nullable=False)
    ID_Vehículo = db.Column(db.Integer, db.ForeignKey('Vehículos.ID_Vehículo'), nullable=False)
    Fecha_compra = db.Column(db.Date, nullable=False)
    Monto = db.Column(db.Numeric(10, 2), nullable=False)

    # Relaciones
    cliente = db.relationship('Cliente', backref='compras')
    vehiculo = db.relationship('Vehiculo', backref='compras')
       
class Inventario(db.Model):
    __tablename__ = 'Inventario'
    
    ID_Inventario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ID_Vehículo = db.Column(db.Integer, db.ForeignKey('Vehiculos.ID_Vehiculo'), nullable=False)
    Ubicación = db.Column(db.String(50), nullable=True)
    Estado = db.Column(db.String(20), nullable=True)

    # Relación con el modelo Vehiculo
    #vehiculo = db.relationship('Vehiculo', backref='inventarios')  
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
            return redirect(url_for('main.panel_control'))  # Redirige al dashboard o página de inicio
        else:
            # Si las credenciales son incorrectas
            flash('Credenciales incorrectas. Intenta de nuevo.', 'error')
            return redirect(url_for('login'))  # Vuelve al formulario de login

    return render_template('login.html')  # Renderiza el formulario de login

# Registrar el blueprint en la aplicación
app.register_blueprint(main_bp) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
