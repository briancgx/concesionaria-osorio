from flask import Blueprint, app, flash, redirect, render_template, request, url_for
from models import db, Cliente, Credito, Inventario, Vehiculo, Compra, Pago, Usuario
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/panel')
def panel_control():
    total_clientes = Cliente.query.filter(Cliente.Estado_cliente == 'Activo').count()
    total_creditos = Credito.query.filter(Credito.Estado_Crédito == 'Aprobado').with_entities(db.func.sum(Credito.Monto_crédito)).scalar() or 0
    total_inventario = Inventario.query.filter(Inventario.Estado == 'Disponible').count()
    total_solicitudes_pendientes = Credito.query.filter(Credito.Estado_Crédito == 'Pendiente').count()  # Contar créditos pendientes
    # Calcular las ventas del mes
    # Calcular las ventas del mes
    fecha_actual = datetime.now()
    primer_dia_mes = datetime(fecha_actual.year, fecha_actual.month, 1)
    ventas_del_mes = Compra.query.with_entities(db.func.sum(db.func.coalesce(Compra.Monto, 0)))\
                             .filter(Compra.Fecha_compra >= primer_dia_mes, Compra.Fecha_compra < fecha_actual)\
                             .scalar() or 0

    pagos_vencidos = Pago.query.filter(Pago.Fecha_pago < fecha_actual, Pago.Estado == 'debe').all()
    inventarios = Inventario.query.all()
    clientes_pendientes = Cliente.query.join(Credito).filter(Credito.Estado_Crédito == 'Pendiente').all()
    return render_template('panel_control.html', total_clientes=total_clientes, total_creditos=total_creditos, total_inventario=total_inventario, ventas_del_mes=ventas_del_mes, total_solicitudes_pendientes=total_solicitudes_pendientes,pagos_vencidos=pagos_vencidos, inventarios=inventarios,clientes_pendientes=clientes_pendientes)

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

@main_bp.route('/creditos2')
def creditos2():
    # Obtener todos los créditos desde la base de datos
    creditos = Credito.query.all()
    
    # Pasar los créditos al template
    return render_template('creditos2.html', creditos=creditos)

@main_bp.route('/creditos3')
def creditos3():
    # Obtener todos los créditos desde la base de datos
    creditos = Credito.query.all()
    
    # Pasar los créditos al template
    return render_template('creditos3.html', creditos=creditos)

@main_bp.route('/inventario')
def inventario():
    # Obtener el término de búsqueda del input
    busqueda = request.args.get('searchInput', '')
    
    if busqueda:
        # Realizar búsqueda por nombre completo del vehículo
        inventarios = Inventario.query.join(Vehiculo).filter(
            db.or_(
                Vehiculo.Marca.ilike(f'%{busqueda}%'),
                Vehiculo.Modelo.ilike(f'%{busqueda}%'),
                db.func.concat(
                    Vehiculo.Marca, ' ', 
                    Vehiculo.Modelo, ' (', 
                    db.cast(Vehiculo.Año, db.String), 
                    ')'
                ).ilike(f'%{busqueda}%')
            )
        ).all()
    else:
        # Si no hay término de búsqueda, mostrar todos los inventarios
        inventarios = Inventario.query.all()
    
    return render_template('inventarios.html', inventarios=inventarios)

@main_bp.route('/inventario2')
def inventario2():
    # Obtener el término de búsqueda del input
    busqueda = request.args.get('searchInput', '')
    
    if busqueda:
        # Realizar búsqueda por marca y modelo del vehículo
        inventarios = Inventario.query.join(Vehiculo).filter(
            db.or_(
                Vehiculo.Marca.ilike(f'%{busqueda}%'),
                Vehiculo.Modelo.ilike(f'%{busqueda}%'),
                db.func.concat(
                    Vehiculo.Marca, ' ', 
                    Vehiculo.Modelo, ' (', 
                    db.cast(Vehiculo.Año, db.String), 
                    ')'
                ).ilike(f'%{busqueda}%')
            )
        ).all()
    else:
        # Si no hay término de búsqueda, mostrar todos los inventarios
        inventarios = Inventario.query.all()
    
    return render_template('inventarios2.html', inventarios=inventarios)

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

# ---------- Créditos ----------

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

# ---------- Usuarios ----------
@main_bp.route('/usuarios')
def usuarios():
    # Obtener todos los usuarios desde la base de datos
    usuarios = Usuario.query.all()
    
    # Pasar los usuarios al template
    return render_template('usuarios.html', usuarios=usuarios)

@main_bp.route('/ver_usuario/<int:id>', methods=['GET'])
def ver_usuario(id):
    # Obtener el usuario por su ID
    usuario = Usuario.query.get_or_404(id)
    
    # Mostrar la información del usuario
    return render_template('ver_usuario.html', usuario=usuario)

@main_bp.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        # Obtener los datos del formulario
        usuario.Nombre_usuario = request.form['nombre_usuario']
        usuario.Contraseña = request.form['contraseña']
        usuario.Rol = request.form['rol']
        
        # Guardar los cambios en la base de datos
        db.session.commit()
        
        flash('Usuario actualizado exitosamente', 'success')
        return redirect(url_for('main.usuarios'))
    
    # Pasar el usuario actual al template para editarlo
    return render_template('editar_usuario.html', usuario=usuario)

@main_bp.route('/eliminar_usuario/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    
    # Eliminar el usuario de la base de datos
    db.session.delete(usuario)
    db.session.commit()
    
    flash('Usuario eliminado', 'danger')
    return redirect(url_for('main.usuarios'))

@main_bp.route('/agregar_usuario', methods=['GET', 'POST'])
def agregar_usuario():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre_usuario = request.form['nombre_usuario']
        contraseña = request.form['contraseña']
        rol = request.form['rol']
        
        # Crear un nuevo usuario
        nuevo_usuario = Usuario(
            Nombre_usuario=nombre_usuario,
            Contraseña=contraseña,
            Rol=rol
        )
        
        # Guardar el usuario en la base de datos
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('Usuario agregado exitosamente', 'success')
        return redirect(url_for('main.usuarios'))
    
    # Mostrar el formulario para agregar un nuevo usuario
    return render_template('agregar_usuario.html')

# ---------- Clientes ----------
@main_bp.route('/clientes')
def clientes():
    # Obtener todos los clientes desde la base de datos
    clientes = Cliente.query.all()
    
    # Pasar los clientes al template
    return render_template('clientes.html', clientes=clientes)

@main_bp.route('/clientes2')
def clientes2():
    # Obtener todos los clientes desde la base de datos
    clientes = Cliente.query.all()
    
    # Pasar los clientes al template
    return render_template('clientes2.html', clientes=clientes)

@main_bp.route('/clientes3')
def clientes3():
    # Obtener todos los clientes desde la base de datos
    clientes = Cliente.query.all()
    
    # Pasar los clientes al template
    return render_template('clientes3.html', clientes=clientes)
@main_bp.route('/nuevo_cliente', methods=['GET', 'POST'])
def nuevo_cliente():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correo = request.form['correo']
        estado = request.form['estado']
        
        # Crear un nuevo cliente
        nuevo_cliente = Cliente(
            Nombre=nombre,
            Dirección=direccion,
            Teléfono=telefono,
            Correo_electrónico=correo,
            Estado_cliente=estado
        )
        
        # Guardar el cliente en la base de datos
        db.session.add(nuevo_cliente)
        db.session.commit()
        
        flash('Cliente agregado exitosamente', 'success')
        return redirect(url_for('main.clientes'))
    
    return render_template('nuevo_cliente.html')

@main_bp.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    if request.method == 'POST':
        # Asegúrate de que el nombre del campo sea correcto
        cliente.Nombre = request.form['nombre']
        cliente.Correo_electrónico = request.form['correo']  # Verifica que 'correo' esté bien escrito
        cliente.Teléfono = request.form['telefono']
        cliente.Dirección = request.form['direccion']
        cliente.Estado_cliente = request.form['estado_cliente']

        db.session.commit()

        flash('Cliente actualizado exitosamente', 'success')
        return redirect(url_for('main.clientes'))

    return render_template('editar_cliente.html', cliente=cliente)

@main_bp.route('/eliminar_cliente/<int:id>', methods=['POST'])
def eliminar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    
    # Eliminar el cliente de la base de datos
    db.session.delete(cliente)
    db.session.commit()
    
    flash('Cliente eliminado', 'danger')
    return redirect(url_for('main.clientes'))

@main_bp.route('/agregar_cliente', methods=['GET', 'POST'])
def agregar_cliente():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        estado_cliente = request.form['estado_cliente']
        
        # Crear un nuevo cliente
        nuevo_cliente = Cliente(
            Nombre=nombre,
            Correo_electrónico=email,
            Teléfono=telefono,
            Dirección=direccion,
            Estado_cliente=estado_cliente
        )
        
        # Guardar el cliente en la base de datos
        db.session.add(nuevo_cliente)
        db.session.commit()
        
        flash('Cliente agregado exitosamente', 'success')
        return redirect(url_for('main.clientes'))
    
    # Si el método es GET, simplemente muestra el formulario
    return render_template('agregar_cliente.html')



@main_bp.route('/panel_gerente')
def panel_gerente():
    total_clientes = Cliente.query.filter(Cliente.Estado_cliente == 'Activo').count()
    total_creditos = Credito.query.filter(Credito.Estado_Crédito == 'Aprobado').with_entities(db.func.sum(Credito.Monto_crédito)).scalar() or 0
    total_inventario = Inventario.query.filter(Inventario.Estado == 'Disponible').count()
    total_solicitudes_pendientes = Credito.query.filter(Credito.Estado_Crédito == 'Pendiente').count()  # Contar créditos pendientes
    # Calcular las ventas del mes
    # Calcular las ventas del mes
    fecha_actual = datetime.now()
    primer_dia_mes = datetime(fecha_actual.year, fecha_actual.month, 1)
    ventas_del_mes = Compra.query.with_entities(db.func.sum(db.func.coalesce(Compra.Monto, 0)))\
                             .filter(Compra.Fecha_compra >= primer_dia_mes, Compra.Fecha_compra < fecha_actual)\
                             .scalar() or 0

    pagos_vencidos = Pago.query.filter(Pago.Fecha_pago < fecha_actual, Pago.Estado == 'debe').all()
    inventarios = Inventario.query.all()
    clientes_pendientes = Cliente.query.join(Credito).filter(Credito.Estado_Crédito == 'Pendiente').all()
    return render_template('panel_gerente.html', total_clientes=total_clientes, total_creditos=total_creditos, total_inventario=total_inventario, ventas_del_mes=ventas_del_mes, total_solicitudes_pendientes=total_solicitudes_pendientes,pagos_vencidos=pagos_vencidos, inventarios=inventarios,clientes_pendientes=clientes_pendientes)
  

@main_bp.route('/panel_asesor')
def panel_asesor():
    # Lógica específica para el asesor de ventas
    return render_template('panel_asesor.html')

@main_bp.route('/panel_asistente')
def panel_asistente():
    # Lógica específica para el asistente administrativo
    return render_template('panel_asistente.html')