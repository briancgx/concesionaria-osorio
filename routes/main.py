from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/clientes')
def clientes():
    return render_template('clientes.html')

@main_bp.route('/panel')
def panel_control():
    return render_template('panel_control.html')

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