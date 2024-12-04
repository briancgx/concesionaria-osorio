from flask import Blueprint, flash, redirect, render_template, request, url_for
from models import db, Cliente, Credito, Inventario, Vehiculo, Compra, Pago
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
    total_solicitudes_pendientes = Credito.query.filter(Credito.Estado_Crédito == 'Pendiente').count()  # Contar créditos pendientes
    # Calcular las ventas del mes
    # Calcular las ventas del mes
    fecha_actual = datetime.now()
    primer_dia_mes = fecha_actual.replace(day=1)
    ventas_del_mes = Compra.query.filter(Compra.Fecha_compra >= primer_dia_mes).with_entities(db.func.sum(Compra.Monto)).scalar() or 0
    pagos_vencidos = Pago.query.filter(Pago.Fecha_pago < fecha_actual).all()
    return render_template('panel_control.html', total_clientes=total_clientes, total_creditos=total_creditos, total_inventario=total_inventario, ventas_del_mes=ventas_del_mes, total_solicitudes_pendientes=total_solicitudes_pendientes,pagos_vencidos=pagos_vencidos)

@main_bp.route('/index')
def index():
    return render_template('index.html')

@main_bp.route('/base')
def base():
    return render_template('base.html')

@main_bp.route('/creditos')
def creditos():
    # Obtener todos los créditos desde la base de datos
    creditos = Credito.query.all()
    
    # Pasar los créditos al template
    return render_template('creditos.html', creditos=creditos)


@main_bp.route('/inventario')
def inventario():
    # Obtener todos los inventarios desde la base de datos
    inventarios = Inventario.query.all()
    
    # Pasar los inventarios al template
    return render_template('inventarios.html', inventarios=inventarios)

@main_bp.route('/ver_inventario/<int:id>', methods=['GET'])
def ver_inventario(id):
    inventario = Inventario.query.get_or_404(id)
    return render_template('ver_inventario.html', inventario=inventario)

@main_bp.route('/editar_inventario/<int:id>', methods=['GET', 'POST'])
def editar_inventario(id):
    inventario = Inventario.query.get_or_404(id)

    if request.method == 'POST':
        # Obtener los datos del formulario
        inventario.Ubicación = request.form['ubicacion']
        inventario.Estado = request.form['estado']
        
        # Guardar los cambios en la base de datos
        db.session.commit()
        
        flash('Inventario actualizado exitosamente', 'success')
        return redirect(url_for('main.inventario'))
    
    return render_template('editar_inventario.html', inventario=inventario)


@main_bp.route('/eliminar_inventario/<int:id>', methods=['POST'])
def eliminar_inventario(id):
    inventario = Inventario.query.get_or_404(id)
    
    # Eliminar el inventario de la base de datos
    db.session.delete(inventario)
    db.session.commit()
    
    flash('Inventario eliminado', 'danger')
    return redirect(url_for('main.inventario'))

@main_bp.route('/agregar_inventario', methods=['GET', 'POST'])
def agregar_inventario():
    if request.method == 'POST':
        # Obtener los datos del formulario
        id_vehiculo = request.form['id_vehiculo']
        ubicacion = request.form['ubicacion']
        estado = request.form['estado']
        
        # Crear un nuevo inventario
        nuevo_inventario = Inventario(
            ID_Vehículo=id_vehiculo,
            Ubicación=ubicacion,
            Estado=estado
        )
        
        # Guardar el inventario en la base de datos
        db.session.add(nuevo_inventario)
        db.session.commit()
        
        flash('Inventario agregado exitosamente', 'success')
        return redirect(url_for('main.inventario'))
    
    # Obtener la lista de vehículos para mostrar en el formulario
    vehiculos = Vehiculo.query.all()

    # Pasar los vehículos al template
    return render_template('agregar_inventario.html', vehiculos=vehiculos)


@main_bp.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')

@main_bp.route('/ver_credito/<int:id>', methods=['GET'])
def ver_credito(id):
    credito = Credito.query.get_or_404(id)
    return render_template('ver_credito.html', credito=credito)

@main_bp.route('/editar_credito/<int:id>', methods=['GET', 'POST'])
def editar_credito(id):
    credito = Credito.query.get_or_404(id)
    if request.method == 'POST':
        # Obtener los datos del formulario
        credito.Monto_crédito = request.form['monto_credito']
        credito.Interés = request.form['interes']
        credito.Fecha_otorgamiento = request.form['fecha_otorgamiento']
        credito.Estado_Crédito = request.form['estado_credito']
        credito.ID_Cliente = request.form['id_cliente']
        
        # Guardar los cambios en la base de datos
        db.session.commit()
        
        flash('Crédito actualizado exitosamente', 'success')
        return redirect(url_for('main.creditos'))
    
    # Obtener la lista de clientes para mostrar en el formulario
    clientes = Cliente.query.all()

    # Pasar el crédito actual y la lista de clientes al template para editarlo
    return render_template('editar_credito.html', credito=credito, clientes=clientes)

@main_bp.route('/aprobar_credito/<int:id>', methods=['POST'])
def aprobar_credito(id):
    credito = Credito.query.get_or_404(id)
    credito.Estado_Crédito = 'Aprobado'
    
    # Guardar los cambios en la base de datos
    db.session.commit()
    
    flash('Crédito aprobado exitosamente', 'success')
    return redirect(url_for('main.creditos'))

@main_bp.route('/rechazar_credito/<int:id>', methods=['POST'])
def rechazar_credito(id):
    credito = Credito.query.get_or_404(id)
    credito.Estado_Crédito = 'Rechazado'
    
    # Guardar los cambios en la base de datos
    db.session.commit()
    
    flash('Crédito rechazado', 'danger')
    return redirect(url_for('main.creditos'))

@main_bp.route('/eliminar_credito/<int:id>', methods=['POST'])
def eliminar_credito(id):
    credito = Credito.query.get_or_404(id)
    
    # Eliminar el crédito de la base de datos
    db.session.delete(credito)
    db.session.commit()
    
    flash('Crédito eliminado', 'danger')
    return redirect(url_for('main.creditos'))


@main_bp.route('/agregar_credito', methods=['GET', 'POST'])
def agregar_credito():
    if request.method == 'POST':
        # Obtener los datos del formulario
        id_cliente = request.form['id_cliente']
        monto_credito = request.form['monto_credito']
        interes = request.form['interes']
        fecha_otorgamiento = request.form['fecha_otorgamiento']
        estado_credito = request.form['estado_credito']
        
        # Crear un nuevo crédito
        nuevo_credito = Credito(
            ID_Cliente=id_cliente,
            Monto_crédito=monto_credito,
            Interés=interes,
            Fecha_otorgamiento=fecha_otorgamiento,
            Estado_Crédito=estado_credito
        )
        
        # Guardar el crédito en la base de datos
        db.session.add(nuevo_credito)
        db.session.commit()
        
        flash('Crédito agregado exitosamente', 'success')
        return redirect(url_for('main.creditos'))
    
    # Obtener la lista de clientes para mostrar en el formulario
    clientes = Cliente.query.all()

    # Pasar los clientes al template
    return render_template('agregar_credito.html', clientes=clientes)
