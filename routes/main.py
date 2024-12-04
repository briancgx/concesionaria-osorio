from flask import Blueprint, render_template
from models import db, Cliente, Credito, Inventario, Vehiculo, Compra
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/clientes')
def clientes():
    return render_template('clientes.html')

@main_bp.route('/panel')
def panel_control():
    total_clientes = Cliente.query.count()
    total_creditos = Credito.query.filter(Credito.Estado_Crédito == 'Aprobado').with_entities(db.func.sum(Credito.Monto_crédito)).scalar() or 0
    total_inventario = Inventario.query.count()
    
    # Calcular las ventas del mes
    fecha_actual = datetime.now()
    primer_dia_mes = fecha_actual.replace(day=1)
    ventas_del_mes = Compra.query.filter(Compra.Fecha_compra >= primer_dia_mes).with_entities(db.func.sum(Compra.Monto)).scalar() or 0

    return render_template('panel_control.html', total_clientes=total_clientes, total_creditos=total_creditos, total_inventario=total_inventario, ventas_del_mes=ventas_del_mes)

@main_bp.route('/index')
def index():
    return render_template('index.html')

@main_bp.route('/base')
def base():
    return render_template('base.html')

@main_bp.route('/creditos')
def creditos():
    return render_template('creditos.html')

@main_bp.route('/inventario')
def inventario():
    return render_template('inventarios.html')

@main_bp.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')
