
from django.shortcuts import render, redirect, get_object_or_404
from .models import Empleado, Prestamo
from .forms import EmpleadoForm, PrestamoForm
from django.urls import reverse

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
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = form.save()  # Guarda el formulario y obtiene la instancia del préstamo
            return redirect(reverse('detalle_prestamo', args=[prestamo.id_prestamo]))  # Redirecciona a la vista de detalle
    else:
        form = PrestamoForm()
    return render(request, 'crear_prestamo.html', {'form': form})

def detalle_prestamo(request, id_prestamo):
    prestamo = Prestamo.objects.get(id_prestamo=id_prestamo)  # Asegúrate de que 'id' es el nombre correcto del campo en tu modelo Prestamo
    cuotas = prestamo.cuotas.all()  # Asume que tienes una relación que permite acceder a 'cuotas' desde un objeto 'prestamo'
    return render(request, 'detalle_prestamo.html', {'prestamo': prestamo, 'cuotas': cuotas})

def listar_prestamo(request):
    prestamos = Prestamo.objects.all()
    return render(request, 'listar_prestamo.html', {'prestamos': prestamos})