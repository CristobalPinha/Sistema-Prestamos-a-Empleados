
from django.shortcuts import render, redirect, get_object_or_404
from .models import Empleado, Prestamo, Cuota
from .forms import EmpleadoForm, PrestamoForm
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
# Crea tus views aqui.

def registrar_empleado(request):
    if request.method == "POST":
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_empleado')
        
    else:
        form = EmpleadoForm()
    return render(request, 'registrar_empleado.html', {'form': form})

def listar_empleado(request):
    empleados = Empleado.objects.all()
    return render(request, 'listar_empleado.html', {'empleados': empleados})

def actualizar_empleado(request, RUT_empleado):
    empleado = get_object_or_404(Empleado, RUT_empleado = RUT_empleado)
    if request.method == "POST":
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('listar_empleado')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'actualizar_empleado.html', {'form': form})

def eliminar_empleado(request, RUT_empleado):
    empleado = Empleado.objects.get(RUT_empleado=RUT_empleado)
    empleado.delete()
    return redirect('listar_empleado')

#==============

def crear_prestamo(request):
    if request.method == "POST":
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = form.save()  # Guardar el préstamo para poder asociar cuotas
            
            monto_cuota = prestamo.monto_pagar / prestamo.cantidad_cuotas
            fecha_emision = timezone.now()  # Asumiendo que la fecha de emisión es la fecha actual
            
            for i in range(1, prestamo.cantidad_cuotas + 1):
                fecha_vencimiento = fecha_emision + timedelta(days=30*i)  # Asumiendo cuotas mensuales
                cuota = Cuota(
                    Prestamo=prestamo,
                    numero_cuota=i,
                    monto_cuota=monto_cuota,
                    cuota_fecha_emision=fecha_emision,
                    cuota_fecha_vencimiento=fecha_vencimiento,
                    cuota_fecha_pago=None  # Inicialmente None, se actualizará cuando se pague la cuota
                )
                cuota.save()
            
            return redirect('listar_prestamo')  # Asegúrate de tener esta ruta definida en urls.py
    else:
        form = PrestamoForm()
    return render(request, 'crear_prestamo.html', {'form': form})

def detalle_prestamo(request, id_prestamo):
    prestamo = Prestamo.objects.get(id_prestamo=id_prestamo)  # Asegúrate de que 'id' es el nombre correcto del campo en tu modelo Prestamo
    cuotas = prestamo.cuotas.all()  # Accede a las cuotas a través de la instancia de prestamo
    return render(request, 'detalle_prestamo.html', {'prestamo': prestamo, 'cuotas': cuotas})

def listar_prestamo(request):
    prestamos = Prestamo.objects.all()
    return render(request, 'listar_prestamo.html', {'prestamos': prestamos})

def eliminar_prestamo(request, id_prestamo):
    prestamo = Prestamo.objects.get(id_prestamo=id_prestamo)
    prestamo.delete()
    return redirect('listar_prestamo')