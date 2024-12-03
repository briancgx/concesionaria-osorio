from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/clientes')
def clientes():
    return render_template('clientes.html')

@main_bp.route('/panel-control')
def panel_control():
    return render_template('panel_control.html')

@main_bp.route('/index')
def index():
    return render_template('index.html')

@main_bp.route('/base')
def base():
    return render_template('base.html')
