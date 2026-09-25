from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, Q
from django.contrib.auth.decorators import login_required
from decimal import Decimal

from .models import Cuenta, Transaccion, Cliente

# --- DASHBOARD ---

@login_required
def dashboard(request):
    # 1. Obtenemos el perfil de cliente del usuario conectado
    cliente_actual = Cliente.objects.filter(usuario=request.user).first()

    # 2. Si el usuario es STAFF / ADMINISTRADOR: ve todas las cuentas y transacciones
    if request.user.is_staff:
        cuentas = Cuenta.objects.all()
        transacciones = Transaccion.objects.all().order_by('-fecha')[:10]
        total_dinero = Cuenta.objects.aggregate(total=Sum('saldo'))['total'] or Decimal('0.00')
        cuenta_propia = Cuenta.objects.filter(cliente=cliente_actual).first() if cliente_actual else None
        saldo_usuario = cuenta_propia.saldo if cuenta_propia else Decimal('0.00')

    # 3. Si es un CLIENTE NORMAL (como Ana López): solo ve SUS cuentas y SUS transacciones
    else:
        if cliente_actual:
            cuentas = Cuenta.objects.filter(cliente=cliente_actual)
            saldo_usuario = cuentas.aggregate(total=Sum('saldo'))['total'] or Decimal('0.00')
            
            transacciones = Transaccion.objects.filter(
                Q(cuenta_origen__cliente=cliente_actual) | Q(cuenta_destino__cliente=cliente_actual)
            ).order_by('-fecha')[:10]
        else:
            cuentas = Cuenta.objects.none()
            transacciones = Transaccion.objects.none()
            saldo_usuario = Decimal('0.00')

        total_dinero = saldo_usuario

    contexto = {
        'cuentas': cuentas,
        'transacciones': transacciones,
        'total_dinero': total_dinero,
        'saldo_usuario': saldo_usuario,
    }
    return render(request, 'gestion/dashboard.html', contexto)


# --- TRANSACCIONES ---

@login_required
def crear_transaccion(request):
    if request.method == 'POST':
        cuenta_origen_id = request.POST.get('cuenta_origen')
        cuenta_destino_id = request.POST.get('cuenta_destino')
        tipo = request.POST.get('tipo')
        monto = Decimal(request.POST.get('monto', 0))
        descripcion = request.POST.get('descripcion', '')

        cuenta_origen = get_object_or_404(Cuenta, id=cuenta_origen_id)

        if tipo in ['RETIRO', 'TRANSFERENCIA'] and cuenta_origen.saldo < monto:
            messages.error(request, "Saldo insuficiente para realizar esta operación.")
            return redirect('crear_transaccion')

        if tipo == 'DEPOSITO':
            cuenta_origen.saldo += monto
            cuenta_origen.save()
            Transaccion.objects.create(cuenta_origen=cuenta_origen, tipo=tipo, monto=monto, descripcion=descripcion)
        elif tipo == 'RETIRO':
            cuenta_origen.saldo -= monto
            cuenta_origen.save()
            Transaccion.objects.create(cuenta_origen=cuenta_origen, tipo=tipo, monto=monto, descripcion=descripcion)
        elif tipo == 'TRANSFERENCIA':
            cuenta_destino = get_object_or_404(Cuenta, id=cuenta_destino_id)
            cuenta_origen.saldo -= monto
            cuenta_destino.saldo += monto
            cuenta_origen.save()
            cuenta_destino.save()
            Transaccion.objects.create(cuenta_origen=cuenta_origen, cuenta_destino=cuenta_destino, tipo=tipo, monto=monto, descripcion=descripcion)

        messages.success(request, "Transacción realizada con éxito.")
        return redirect('dashboard')

    # Para cargar el formulario, mostramos las cuentas que le corresponden según su rol
    if request.user.is_staff:
        cuentas = Cuenta.objects.all()
    else:
        cliente_actual = Cliente.objects.filter(usuario=request.user).first()
        cuentas = Cuenta.objects.filter(cliente=cliente_actual) if cliente_actual else Cuenta.objects.none()

    return render(request, 'gestion/crear_transaccion.html', {'cuentas': cuentas})


@login_required
def realizar_transferencia(request):
    if request.method == 'POST':
        monto = Decimal(request.POST.get('monto', '0'))
        cuenta_destino_id = request.POST.get('cuenta_destino')

        if monto <= 0:
            messages.warning(request, "El monto debe ser mayor a $0.")
            return redirect('crear_transaccion')

        try:
            with transaction.atomic():
                cuenta_origen = Cuenta.objects.select_for_update().get(cliente__usuario=request.user)
                cuenta_destino = Cuenta.objects.select_for_update().get(id=cuenta_destino_id)

                if cuenta_origen.saldo < monto:
                    messages.error(request, "Saldo insuficiente para realizar esta transferencia.")
                    return redirect('crear_transaccion')

                cuenta_origen.saldo -= monto
                cuenta_destino.saldo += monto
                cuenta_origen.save()
                cuenta_destino.save()

                Transaccion.objects.create(
                    cuenta_origen=cuenta_origen,
                    cuenta_destino=cuenta_destino,
                    monto=monto,
                    tipo='TRANSFERENCIA'
                )

                messages.success(request, f"¡Transferencia de ${monto} realizada con éxito!")
                return redirect('dashboard')

        except Cuenta.DoesNotExist:
            messages.error(request, "La cuenta seleccionada no existe o no tienes permisos.")
        except Exception as e:
            messages.error(request, "Ocurrió un error inesperado. Inténtelo nuevamente.")

    return render(request, 'gestion/crear_transaccion.html')


# --- CRUD DE CLIENTES ---

def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('id')
    return render(request, 'gestion/lista_clientes.html', {'clientes': clientes})

def crear_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')

        cliente = Cliente.objects.create(nombre=nombre, email=email, telefono=telefono)
        messages.success(request, f"Cliente N° {cliente.id} ({cliente.nombre}) creado correctamente.")
        return redirect('lista_clientes')

    return render(request, 'gestion/form_cliente.html')

def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre')
        cliente.email = request.POST.get('email')
        cliente.telefono = request.POST.get('telefono')
        cliente.save()
        messages.success(request, f"Datos del Cliente N° {cliente.id} ({cliente.nombre}) actualizados correctamente.")
        return redirect('lista_clientes')

    return render(request, 'gestion/form_cliente.html', {'cliente': cliente})

def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    nombre_cliente = cliente.nombre
    id_cliente = cliente.id
    cliente.delete()
    messages.success(request, f"Cliente N° {id_cliente} ({nombre_cliente}) eliminado con éxito.")
    return redirect('lista_clientes')


# --- CRUD DE CUENTAS ---

def crear_cuenta(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        numero_cuenta = request.POST.get('numero_cuenta')
        tipo_cuenta = request.POST.get('tipo_cuenta')
        saldo = Decimal(request.POST.get('saldo', 0))

        cliente = get_object_or_404(Cliente, id=cliente_id)
        Cuenta.objects.create(cliente=cliente, numero_cuenta=numero_cuenta, tipo_cuenta=tipo_cuenta, saldo=saldo)
        messages.success(request, "Cuenta creada exitosamente.")
        return redirect('dashboard')

    clientes = Cliente.objects.all()
    return render(request, 'gestion/form_cuenta.html', {'clientes': clientes})

def eliminar_cuenta(request, id):
    cuenta = get_object_or_404(Cuenta, id=id)
    cuenta.delete()
    messages.success(request, "Cuenta eliminada correctamente.")
    return redirect('dashboard')

def detalle_cuenta(request, id):
    cuenta = get_object_or_404(Cuenta, id=id)
    
    transacciones_origen = Transaccion.objects.filter(cuenta_origen=cuenta)
    transacciones_destino = Transaccion.objects.filter(cuenta_destino=cuenta)
    transacciones = (transacciones_origen | transacciones_destino).distinct().order_by('-fecha')

    context = {
        'cuenta': cuenta,
        'transacciones': transacciones,
    }
    return render(request, 'gestion/detalle_cuenta.html', context)