from flask_sqlalchemy import SQLAlchemy

# Crear la instancia de SQLAlchemy
db = SQLAlchemy()

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

# Definición del modelo para la tabla Créditos
class Credito(db.Model):
    __tablename__ = 'Créditos'
    
    ID_Crédito = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ID_Cliente = db.Column(db.Integer, db.ForeignKey('Clientes.ID_Cliente'), nullable=False)
    Monto_crédito = db.Column(db.Numeric(10, 2), nullable=True)
    Interés = db.Column(db.Numeric(4, 2), nullable=True)
    Fecha_otorgamiento = db.Column(db.Date, nullable=True)
    Estado_Crédito = db.Column(db.String(10), nullable=True)

    # Relación con el modelo Cliente
    cliente = db.relationship('Cliente', backref='creditos')

# Definición del modelo para la tabla Vehículos
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

# Definición del modelo para la tabla Compras
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

# Definición del modelo para la tabla Inventario
class Inventario(db.Model):
    __tablename__ = 'Inventario'
    
    ID_Inventario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ID_Vehículo = db.Column(db.Integer, db.ForeignKey('Vehículos.ID_Vehículo'), nullable=False)
    Ubicación = db.Column(db.String(50), nullable=True)
    Estado = db.Column(db.String(20), nullable=True)

    # Relación con el modelo Vehiculo
    vehiculo = db.relationship('Vehiculo', backref='inventarios')


class AtencionAlCliente(db.Model):
    __tablename__ = 'Atención_al_Cliente'

    ID_Atención = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ID_Cliente = db.Column(db.Integer, db.ForeignKey('Clientes.ID_Cliente'), nullable=True)
    Fecha_atención = db.Column(db.Date, nullable=True)
    Descripción = db.Column(db.Text, nullable=True)
    Resolución = db.Column(db.Text, nullable=True)

    # Relación con el modelo Cliente
    cliente = db.relationship('Cliente', backref='atenciones')

class HistorialCredito(db.Model):
    __tablename__ = 'Historial_Crédito'

    ID_Historial = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ID_Crédito = db.Column(db.Integer, db.ForeignKey('Créditos.ID_Crédito'), nullable=True)  # Asegúrate de usar 'ID_Crédito' aquí
    Fecha_actualización = db.Column(db.Date, nullable=True)
    Estado = db.Column(db.String(20), nullable=True)

    # Relación con el modelo Crédito
    credito = db.relationship('Credito', backref='historiales')


class Pago(db.Model):
    __tablename__ = 'Pagos'

    ID_Pago = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ID_Crédito = db.Column(db.Integer, db.ForeignKey('Créditos.ID_Crédito'), nullable=True)
    Monto_pago = db.Column(db.Numeric(10, 2), nullable=True)
    Fecha_pago = db.Column(db.Date, nullable=True)
    Estado = db.Column(db.String(4), nullable=True) 
    # Relación con el modelo Crédito
    credito = db.relationship('Credito', backref='pagos')

class Reporte(db.Model):
    __tablename__ = 'Reportes'

    ID_Reporte = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ID_Usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.ID_Usuario'), nullable=True)
    Fecha = db.Column(db.Date, nullable=True)
    Tipo = db.Column(db.String(50), nullable=True)
    Descripción = db.Column(db.Text, nullable=True)

    # Relación con el modelo Usuario
    usuario = db.relationship('Usuario', backref='reportes')
