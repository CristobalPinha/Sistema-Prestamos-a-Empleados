from django.shortcuts import render, redirect, get_object_or_404
from .models import Empleado, Prestamo
from .forms import EmpleadoForm, PrestamoForm
from .services import generar_cuotas


def employee_list(request):
    empleados = Empleado.objects.all()
    return render(request, 'employee_list.html', {'empleados': empleados})


def employee_create(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmpleadoForm()
    return render(request, 'employee_create.html', {'form': form})


def employee_update(request, RUT_empleado):
    empleado = get_object_or_404(Empleado, RUT_empleado=RUT_empleado)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'employee_update.html', {'form': form})


def employee_delete(request, RUT_empleado):
    empleado = get_object_or_404(Empleado, RUT_empleado=RUT_empleado)
    empleado.delete()
    return redirect('employee_list')


def loan_list(request):
    prestamos = Prestamo.objects.all()
    return render(request, 'loan_list.html', {'prestamos': prestamos})


def loan_create(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = form.save()
            generar_cuotas(prestamo)
            return redirect('loan_list')
    else:
        form = PrestamoForm()
    return render(request, 'loan_create.html', {'form': form})


def loan_detail(request, id_prestamo):
    prestamo = get_object_or_404(Prestamo, id_prestamo=id_prestamo)
    cuotas = prestamo.cuotas.all()
    return render(request, 'loan_detail.html', {'prestamo': prestamo, 'cuotas': cuotas})


def loan_delete(request, id_prestamo):
    prestamo = get_object_or_404(Prestamo, id_prestamo=id_prestamo)
    prestamo.delete()
    return redirect('loan_list')
