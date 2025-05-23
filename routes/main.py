from flask import Blueprint, app, flash, redirect, render_template, request, url_for,session
from sqlalchemy import extract
from models import db, Cliente, Credito, Inventario, Vehiculo, Compra, Pago, Usuario
from collections import Counter
from collections import defaultdict
from decimal import Decimal
from datetime import datetime
from sqlalchemy import func
from flask import send_file               # ← Para devolver el PDF como respuesta
from io import BytesIO                    # ← Para generar el PDF en memoria
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/panel')
def panel_control():
    session['panel_origen'] = request.path 
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
    # 🟢 VENTAS POR MES DINÁMICO (ahora sí JSON-serializable)
    ventas_query = db.session.query(
        extract('month', Compra.Fecha_compra).label('mes'),
        db.func.sum(Compra.Monto).label('total')
    ).group_by('mes').order_by('mes').all()

    ventas_por_mes = [{'mes': mes, 'total': float(total)} for mes, total in ventas_query]

    # 🟢 CRÉDITOS POR MES DINÁMICO
    creditos_query = db.session.query(
        extract('month', Credito.Fecha_otorgamiento).label('mes'),
        db.func.sum(Credito.Monto_crédito).label('total')
    ).filter(Credito.Estado_Crédito == 'Aprobado')\
     .group_by('mes').order_by('mes').all()

    creditos_por_mes = [{'mes': mes, 'total': float(total)} for mes, total in creditos_query]

    return render_template('panel_control.html', total_clientes=total_clientes, total_creditos=total_creditos, total_inventario=total_inventario, ventas_del_mes=ventas_del_mes, total_solicitudes_pendientes=total_solicitudes_pendientes,pagos_vencidos=pagos_vencidos, inventarios=inventarios,clientes_pendientes=clientes_pendientes,ventas_por_mes=ventas_por_mes,creditos_por_mes=creditos_por_mes)

@main_bp.route('/index')
def index():
    return render_template('index.html')

@main_bp.route('/base')
def base():
    return render_template('base.html')

@main_bp.route('/creditos')
def creditos():
    # 👇 ESTA línea es crítica
    creditos = Credito.query.all()

    # Distribución por estado
    estados = [c.Estado_Crédito for c in creditos]
    creditos_por_estado = dict(Counter(estados))

    # Suma de montos por cliente
    creditos_por_cliente = {}
    for c in creditos:
        nombre = c.cliente.Nombre
        creditos_por_cliente[nombre] = creditos_por_cliente.get(nombre, 0) + float(c.Monto_crédito)

    return render_template('creditos.html', creditos=creditos,
                           creditos_por_estado=creditos_por_estado,
                           creditos_por_cliente=creditos_por_cliente)



@main_bp.route('/creditos2')
def creditos2():
    # Obtener todos los créditos desde la base de datos
    creditos = Credito.query.all()
    estados = [c.Estado_Crédito for c in creditos]
    creditos_por_estado = dict(Counter(estados))

    # Suma de montos por cliente
    creditos_por_cliente = {}
    for c in creditos:
        nombre = c.cliente.Nombre
        creditos_por_cliente[nombre] = creditos_por_cliente.get(nombre, 0) + float(c.Monto_crédito)

    return render_template('creditos2.html', creditos=creditos,
                           creditos_por_estado=creditos_por_estado,
                           creditos_por_cliente=creditos_por_cliente)

@main_bp.route('/creditos3')
def creditos3():
    # Obtener todos los créditos desde la base de datos
    creditos = Credito.query.all()
    
    estados = [c.Estado_Crédito for c in creditos]
    creditos_por_estado = dict(Counter(estados))

    # Suma de montos por cliente
    creditos_por_cliente = {}
    for c in creditos:
        nombre = c.cliente.Nombre
        creditos_por_cliente[nombre] = creditos_por_cliente.get(nombre, 0) + float(c.Monto_crédito)

    return render_template('creditos3.html', creditos=creditos,
                           creditos_por_estado=creditos_por_estado,
                           creditos_por_cliente=creditos_por_cliente)
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
    
    # Lógica para gráficas dinámicas
    inventarios_por_estado = {}
    inventarios_por_ubicacion = {}

    for inv in inventarios:
        # Contar por estado
        estado = inv.Estado
        inventarios_por_estado[estado] = inventarios_por_estado.get(estado, 0) + 1

        # Contar por ubicación
        ubicacion = inv.Ubicación
        inventarios_por_ubicacion[ubicacion] = inventarios_por_ubicacion.get(ubicacion, 0) + 1

    # Retornar todo a la plantilla
    return render_template(
        'inventarios.html',
        inventarios=inventarios,
        inventarios_por_estado=inventarios_por_estado,
        inventarios_por_ubicacion=inventarios_por_ubicacion
    )


@main_bp.route('/inventario2')
def inventario2():
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
    
    # Lógica para gráficas dinámicas
    inventarios_por_estado = {}
    inventarios_por_ubicacion = {}

    for inv in inventarios:
        # Contar por estado
        estado = inv.Estado
        inventarios_por_estado[estado] = inventarios_por_estado.get(estado, 0) + 1

        # Contar por ubicación
        ubicacion = inv.Ubicación
        inventarios_por_ubicacion[ubicacion] = inventarios_por_ubicacion.get(ubicacion, 0) + 1

    # Retornar todo a la plantilla
    return render_template(
        'inventarios.html',
        inventarios=inventarios,
        inventarios_por_estado=inventarios_por_estado,
        inventarios_por_ubicacion=inventarios_por_ubicacion
    )


@main_bp.route('/ver_inventario/<int:id>', methods=['GET'])
def ver_inventario(id):
    inventario = Inventario.query.get_or_404(id)
    return render_template('ver_inventario.html', inventario=inventario)

@main_bp.route('/editar_inventario/<int:id>', methods=['GET', 'POST'])
def editar_inventario(id):
    inventario = Inventario.query.get_or_404(id)
    vehiculo = inventario.vehiculo

    if request.method == 'POST':
        # Actualizar datos del vehículo vinculado
        vehiculo.Marca = request.form['marca']
        vehiculo.Modelo = request.form['modelo']
        vehiculo.Año = int(request.form['año'])

        # Actualizar datos del inventario
        inventario.Ubicación = request.form['ubicacion']
        inventario.Estado = request.form['estado']

        db.session.commit()
        flash('Inventario actualizado correctamente', 'success')
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
        import re

        # Obtener los datos del formulario
        vehiculo_str = request.form['vehiculo']
        ubicacion = request.form['ubicacion']
        estado = request.form['estado']

        # Extraer marca, modelo y año con regex
        match = re.match(r'^(.+?)\s+(.+?)\s+\((\d{4})\)$', vehiculo_str)

        if not match:
            flash('Formato inválido. Usa: Marca Modelo (Año)', 'error')
            return redirect(url_for('main.agregar_inventario'))

        marca = match.group(1).strip()
        modelo = match.group(2).strip()
        año = int(match.group(3))

   
        vehiculo = Vehiculo(Marca=marca, Modelo=modelo, Año=año)
        db.session.add(vehiculo)
        db.session.commit()

        id_vehiculo = vehiculo.ID_Vehículo

        # Crear nuevo inventario
        nuevo_inventario = Inventario(
            ID_Vehículo=id_vehiculo,
            Ubicación=ubicacion,
            Estado=estado
        )
        db.session.add(nuevo_inventario)
        db.session.commit()

        flash('Inventario agregado exitosamente', 'success')
        return redirect(url_for('main.inventario'))

    # GET: Cargar vehículos existentes para mostrar en el datalist
    vehiculos = Vehiculo.query.all()
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
    roles = defaultdict(int)
    for u in usuarios:
        roles[u.Rol] += 1
    # Pasar los usuarios al template
    return render_template('usuarios.html', usuarios=usuarios, usuarios_por_rol=roles)

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

from datetime import datetime
from flask import render_template

@main_bp.route('/agregar_usuario', methods=['GET', 'POST'])
def agregar_usuario():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        contraseña = request.form['contraseña']
        rol = request.form['rol']
        fecha_creacion = request.form.get('fecha_creacion', datetime.utcnow())
        ultimo_acceso = request.form.get('ultimo_acceso', datetime.utcnow())

        nuevo_usuario = Usuario(
            Nombre_usuario=nombre_usuario,
            Contraseña=contraseña,
            Rol=rol,
            Fecha_creacion=fecha_creacion,
            Ultimo_acceso=ultimo_acceso
        )
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('main.usuarios'))
    
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M')
    return render_template('agregar_usuario.html', current_time=current_time)

# ---------- Clientes ----------
@main_bp.route('/clientes')
def clientes():
    # Obtener todos los clientes desde la base de datos
    clientes = Cliente.query.all()
    estado_data = {}
    for cliente in clientes:
        estado = cliente.Estado_cliente
        estado_data[estado] = estado_data.get(estado, 0) + 1
    # Pasar los clientes al template
    return render_template('clientes.html', clientes=clientes, clientes_por_estado=estado_data)

@main_bp.route('/clientes2')
def clientes2():
    # Obtener todos los clientes desde la base de datos
    clientes = Cliente.query.all()
    estado_data = {}
    for cliente in clientes:
        estado = cliente.Estado_cliente
        estado_data[estado] = estado_data.get(estado, 0) + 1
    # Pasar los clientes al template
    return render_template('clientes2.html', clientes=clientes, clientes_por_estado=estado_data)

@main_bp.route('/clientes3')
def clientes3():
    # Obtener todos los clientes desde la base de datos
    clientes = Cliente.query.all()
    estado_data = {}
    for cliente in clientes:
        estado = cliente.Estado_cliente
        estado_data[estado] = estado_data.get(estado, 0) + 1
    # Pasar los clientes al template
    return render_template('clientes3.html', clientes=clientes, clientes_por_estado=estado_data)
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
    next_url = request.args.get('next') or url_for('main.clientes')
    return redirect(next_url)

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
    session['panel_origen'] = request.path
    fecha_actual = datetime.now()
    primer_dia_mes = datetime(fecha_actual.year, fecha_actual.month, 1)

    total_clientes = Cliente.query.filter(Cliente.Estado_cliente == 'Activo').count()
    total_creditos = Credito.query.filter(Credito.Estado_Crédito == 'Aprobado')\
        .with_entities(db.func.sum(Credito.Monto_crédito)).scalar() or 0
    total_inventario = Inventario.query.filter(Inventario.Estado == 'Disponible').count()
    total_solicitudes_pendientes = Credito.query.filter(Credito.Estado_Crédito == 'Pendiente').count()
    ventas_del_mes = Compra.query.with_entities(db.func.sum(db.func.coalesce(Compra.Monto, 0)))\
        .filter(Compra.Fecha_compra >= primer_dia_mes, Compra.Fecha_compra < fecha_actual).scalar() or 0

    # Datos adicionales
    pagos_vencidos = Pago.query.filter(Pago.Fecha_pago < fecha_actual, Pago.Estado == 'debe').all()
    pagos_realizados = Pago.query.filter(Pago.Estado == 'Pago').all()
    compras_realizadas = Compra.query.all()
    inventarios = Inventario.query.all()
    clientes_pendientes = Cliente.query.join(Credito).filter(Credito.Estado_Crédito == 'Pendiente').all()

    # Gráficas
    ventas_query = db.session.query(
        extract('month', Compra.Fecha_compra).label('mes'),
        db.func.sum(Compra.Monto).label('total')
    ).group_by('mes').order_by('mes').all()

    ventas_por_mes = [{'mes': mes, 'total': float(total)} for mes, total in ventas_query]

    creditos_query = db.session.query(
        extract('month', Credito.Fecha_otorgamiento).label('mes'),
        db.func.sum(Credito.Monto_crédito).label('total')
    ).filter(Credito.Estado_Crédito == 'Aprobado').group_by('mes').order_by('mes').all()

    creditos_por_mes = [{'mes': mes, 'total': float(total)} for mes, total in creditos_query]

    # Créditos pagados o con abonos
    creditos = Credito.query.all()
    creditos_pagados = []
    creditos_con_pagos = []

    for credito in creditos:
        suma_pagos = db.session.query(db.func.sum(Pago.Monto_pago))\
            .filter(Pago.ID_Crédito == credito.ID_Crédito).scalar() or Decimal('0')

        if suma_pagos >= credito.Monto_crédito:
            creditos_pagados.append((credito.cliente.Nombre, credito.ID_Crédito))
        elif suma_pagos > 0:
            creditos_con_pagos.append((credito.cliente.Nombre, credito.ID_Crédito, float(suma_pagos), float(credito.Monto_crédito)))

    return render_template('panel_gerente.html',
        total_clientes=total_clientes,
        total_creditos=total_creditos,
        total_inventario=total_inventario,
        ventas_del_mes=ventas_del_mes,
        total_solicitudes_pendientes=total_solicitudes_pendientes,
        pagos_vencidos=pagos_vencidos,
        pagos_realizados=pagos_realizados,
        compras_realizadas=compras_realizadas,
        inventarios=inventarios,
        clientes_pendientes=clientes_pendientes,
        ventas_por_mes=ventas_por_mes,
        creditos_por_mes=creditos_por_mes,
        creditos_pagados=creditos_pagados,
        creditos_con_pagos=creditos_con_pagos
    )

@main_bp.route('/panel_asesor')
def panel_asesor():
    session['panel_origen'] = request.path 
    fecha_actual = datetime.now()
    primer_dia_mes = datetime(fecha_actual.year, fecha_actual.month, 1)

    total_clientes = Cliente.query.filter(Cliente.Estado_cliente == 'Activo').count()
    total_creditos = Credito.query.filter(Credito.Estado_Crédito == 'Aprobado')\
                         .with_entities(db.func.sum(Credito.Monto_crédito)).scalar() or 0
    total_inventario = Inventario.query.filter(Inventario.Estado == 'Disponible').count()
    total_solicitudes_pendientes = Credito.query.filter(Credito.Estado_Crédito == 'Pendiente').count()

    ventas_del_mes = Compra.query.with_entities(db.func.sum(db.func.coalesce(Compra.Monto, 0)))\
                         .filter(Compra.Fecha_compra >= primer_dia_mes, Compra.Fecha_compra < fecha_actual)\
                         .scalar() or 0

    # 🔔 NUEVAS LISTAS PARA ALERTAS
    pagos_vencidos = Pago.query.filter(Pago.Fecha_pago < fecha_actual, Pago.Estado == 'debe').all()
    pagos_realizados = Pago.query.filter(Pago.Fecha_pago >= primer_dia_mes).all()
    compras_recientes = Compra.query.filter(Compra.Fecha_compra >= primer_dia_mes).all()
    inventarios = Inventario.query.all()
    clientes_pendientes = Cliente.query.join(Credito).filter(Credito.Estado_Crédito == 'Pendiente').all()

    # 🔢 Gráficas: ventas por mes
    ventas_query = db.session.query(
        extract('month', Compra.Fecha_compra).label('mes'),
        db.func.sum(Compra.Monto).label('total')
    ).group_by('mes').order_by('mes').all()

    ventas_por_mes = [{'mes': mes, 'total': float(total)} for mes, total in ventas_query]

    # 🔢 Gráficas: créditos por mes
    creditos_query = db.session.query(
        extract('month', Credito.Fecha_otorgamiento).label('mes'),
        db.func.sum(Credito.Monto_crédito).label('total')
    ).filter(Credito.Estado_Crédito == 'Aprobado')\
     .group_by('mes').order_by('mes').all()

    creditos_por_mes = [{'mes': mes, 'total': float(total)} for mes, total in creditos_query]

    return render_template('panel_asesor.html',
        total_clientes=total_clientes,
        total_creditos=total_creditos,
        total_inventario=total_inventario,
        ventas_del_mes=ventas_del_mes,
        total_solicitudes_pendientes=total_solicitudes_pendientes,
        pagos_vencidos=pagos_vencidos,
        pagos_realizados=pagos_realizados,
        compras_recientes=compras_recientes,
        inventarios=inventarios,
        clientes_pendientes=clientes_pendientes,
        ventas_por_mes=ventas_por_mes,
        creditos_por_mes=creditos_por_mes
    )
@main_bp.route('/panel_asistente')
def panel_asistente():
    session['panel_origen'] = request.path 
    fecha_actual = datetime.now()
    primer_dia_mes = datetime(fecha_actual.year, fecha_actual.month, 1)

    total_clientes = Cliente.query.filter(Cliente.Estado_cliente == 'Activo').count()
    total_creditos = Credito.query.filter(Credito.Estado_Crédito == 'Aprobado')\
                         .with_entities(db.func.sum(Credito.Monto_crédito)).scalar() or 0
    total_inventario = Inventario.query.filter(Inventario.Estado == 'Disponible').count()
    total_solicitudes_pendientes = Credito.query.filter(Credito.Estado_Crédito == 'Pendiente').count()

    ventas_del_mes = Compra.query.with_entities(db.func.sum(db.func.coalesce(Compra.Monto, 0)))\
                         .filter(Compra.Fecha_compra >= primer_dia_mes, Compra.Fecha_compra < fecha_actual)\
                         .scalar() or 0

    pagos_vencidos = Pago.query.filter(Pago.Fecha_pago < fecha_actual, Pago.Estado == 'debe').all()
    pagos_realizados = Pago.query.filter(Pago.Fecha_pago >= primer_dia_mes).all()

    inventarios = Inventario.query.all()
    clientes_pendientes = Cliente.query.join(Credito).filter(Credito.Estado_Crédito == 'Pendiente').all()

    ventas_query = db.session.query(
        extract('month', Compra.Fecha_compra).label('mes'),
        db.func.sum(Compra.Monto).label('total')
    ).group_by('mes').order_by('mes').all()

    ventas_por_mes = [{'mes': mes, 'total': float(total)} for mes, total in ventas_query]

    creditos_query = db.session.query(
        extract('month', Credito.Fecha_otorgamiento).label('mes'),
        db.func.sum(Credito.Monto_crédito).label('total')
    ).filter(Credito.Estado_Crédito == 'Aprobado')\
     .group_by('mes').order_by('mes').all()

    creditos_por_mes = [{'mes': mes, 'total': float(total)} for mes, total in creditos_query]

    creditos = Credito.query.all()
    creditos_pagados = []
    creditos_con_pagos = []

    for credito in creditos:
        suma_pagos = db.session.query(db.func.sum(Pago.Monto_pago))\
            .filter(Pago.ID_Crédito == credito.ID_Crédito).scalar() or Decimal('0')

        if suma_pagos >= credito.Monto_crédito:
            creditos_pagados.append((credito.cliente.Nombre, credito.ID_Crédito))
        elif suma_pagos > 0:
            creditos_con_pagos.append((credito.cliente.Nombre, credito.ID_Crédito, float(suma_pagos), float(credito.Monto_crédito)))

    return render_template('panel_asistente.html',
        total_clientes=total_clientes,
        total_creditos=total_creditos,
        total_inventario=total_inventario,
        ventas_del_mes=ventas_del_mes,
        total_solicitudes_pendientes=total_solicitudes_pendientes,
        pagos_vencidos=pagos_vencidos,
        pagos_realizados=pagos_realizados,  # 🟡 Agregado
        inventarios=inventarios,
        clientes_pendientes=clientes_pendientes,
        ventas_por_mes=ventas_por_mes,
        creditos_por_mes=creditos_por_mes,
        creditos_pagados=creditos_pagados,
        creditos_con_pagos=creditos_con_pagos
    )

@main_bp.route('/compras', methods=['GET', 'POST'])
def ver_compras():
    if request.method == 'POST':
        nueva_compra = Compra(
            ID_Cliente=request.form['cliente_id'],
            ID_Vehículo=request.form['vehiculo_id'],
            Fecha_compra=request.form['fecha_compra'],
            Monto=request.form['monto']
        )
        db.session.add(nueva_compra)
        db.session.commit()
        return redirect(url_for('main.ver_compras'))

    compras = Compra.query.all()
    clientes = Cliente.query.all()
    vehiculos = Vehiculo.query.all()

    # Gráfica: compras por vehículo
    compras_por_vehiculo = {}
    for compra in compras:
        if compra.vehiculo:
            nombre = f"{compra.vehiculo.Marca} {compra.vehiculo.Modelo} {compra.vehiculo.Año}"
            compras_por_vehiculo[nombre] = compras_por_vehiculo.get(nombre, 0) + 1

    # Gráfica: compras por mes (formato MM)
    compras_query = db.session.query(
        extract('month', Compra.Fecha_compra).label('mes'),
        db.func.count(Compra.ID_Compra).label('total')
    ).group_by('mes').order_by('mes').all()

    compras_por_mes = {
        f"{int(mes):02d}": total for mes, total in compras_query if mes is not None
    }

    return render_template(
        "compras.html",
        compras=compras,
        clientes=clientes,
        vehiculos=vehiculos,
        compras_por_vehiculo=compras_por_vehiculo,
        compras_por_mes=compras_por_mes  # <- Aquí se pasa correctamente
    )

@main_bp.route('/eliminar_compra/<int:id>', methods=['POST'])
def eliminar_compra(id):
    compra = Compra.query.get_or_404(id)
    db.session.delete(compra)
    db.session.commit()
    return redirect(url_for('main.ver_compras'))
   
@main_bp.route('/pagos', methods=['GET', 'POST'])
def ver_pagos():
    if request.method == 'POST':
        credito_id = int(request.form['credito_id'])
        monto_pago = Decimal(request.form['monto_pago'])
        fecha_pago = request.form['fecha_pago']

        credito = Credito.query.get(credito_id)
        if not credito:
            return "Crédito no encontrado", 404

        # Sumar pagos anteriores
        total_anterior = db.session.query(db.func.sum(Pago.Monto_pago))\
            .filter(Pago.ID_Crédito == credito_id).scalar() or Decimal('0')
        
        total_acumulado = total_anterior + monto_pago

        # Determinar estado
        estado = 'Pago' if total_acumulado >= credito.Monto_crédito else 'Debe'

        # Crear el nuevo pago
        nuevo_pago = Pago(
            ID_Crédito=credito_id,
            Fecha_pago=fecha_pago,
            Monto_pago=monto_pago,
            Estado=estado
        )
        db.session.add(nuevo_pago)

        # Si se completó el crédito, actualizar todos los pagos de ese crédito a "Pago"
        if estado == 'Pago':
            pagos_previos = Pago.query.filter(Pago.ID_Crédito == credito_id).all()
            for pago in pagos_previos:
                pago.Estado = 'Pago'

        db.session.commit()
        return redirect(url_for('main.ver_pagos'))

    pagos = Pago.query.all()
    creditos = Credito.query.all()
    return render_template("pagos.html", pagos=pagos, creditos=creditos)



@main_bp.route('/eliminar_pago/<int:id>', methods=['POST'])
def eliminar_pago(id):
    pago = Pago.query.get_or_404(id)
    db.session.delete(pago)
    db.session.commit()
    return redirect(url_for('main.ver_pagos'))


@main_bp.route('/formulario_reporte')
def formulario_reporte():
    return render_template('formulario_reporte.html')


@main_bp.route('/reporte_ventas_pdf', methods=['GET', 'POST'])
def reporte_ventas_pdf():
    if request.method == 'POST':
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']

        ventas = db.session.query(Compra, Cliente, Vehiculo)\
            .join(Cliente, Compra.ID_Cliente == Cliente.ID_Cliente)\
            .join(Vehiculo, Compra.ID_Vehículo == Vehiculo.ID_Vehículo)\
            .filter(Compra.Fecha_compra.between(fecha_inicio, fecha_fin))\
            .all()

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        elements.append(Paragraph("Reporte de Ventas", styles['Title']))
        elements.append(Spacer(1, 12))

        data = [['Cliente', 'Vehículo', 'Fecha de Compra', 'Monto']]
        total = 0

        for compra, cliente, vehiculo in ventas:
            fila = [
                cliente.Nombre,
                f"{vehiculo.Marca} {vehiculo.Modelo}",
                compra.Fecha_compra.strftime('%Y-%m-%d'),
                f"${compra.Monto:,.2f}"
            ]
            total += compra.Monto
            data.append(fila)

        data.append(['', '', 'Total:', f"${total:,.2f}"])

        table = Table(data, hAlign='LEFT')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (-2, 1), (-1, -2), 'RIGHT'),
            ('ALIGN', (-1, -1), (-1, -1), 'RIGHT'),
            ('SPAN', (0, -1), (-3, -1)),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ]))

        elements.append(table)
        doc.build(elements)

        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='reporte_ventas.pdf', mimetype='application/pdf')
    else:
        return redirect(url_for('main.formulario_reporte'))
