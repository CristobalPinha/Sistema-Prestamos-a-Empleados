from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Empleado, Prestamo, Cuota, TipoPrestamo, Comuna
from .forms import EmpleadoForm, PrestamoForm
from .serializers import EmpleadoSerializer, PrestamoSerializer, CuotaSerializer, TipoPrestamoSerializer, ComunaSerializer
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


# ─── API REST ────────────────────────────────────────────────────────────────

class EmpleadoViewSet(viewsets.ModelViewSet):
    # ModelViewSet genera automáticamente: list, retrieve, create, update, destroy
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer


class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer

    # Acción extra: GET /api/prestamos/{id}/cuotas/
    # Sin esto, las cuotas solo aparecen anidadas dentro del préstamo
    @action(detail=True, methods=['get'])
    def cuotas(self, request, pk=None):
        prestamo = self.get_object()
        cuotas = prestamo.cuotas.all()
        serializer = CuotaSerializer(cuotas, many=True)
        return Response(serializer.data)


class TipoPrestamoViewSet(viewsets.ModelViewSet):
    queryset = TipoPrestamo.objects.all()
    serializer_class = TipoPrestamoSerializer


class ComunaViewSet(viewsets.ModelViewSet):
    queryset = Comuna.objects.all()
    serializer_class = ComunaSerializer
