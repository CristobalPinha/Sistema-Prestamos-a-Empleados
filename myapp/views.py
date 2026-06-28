from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Sum
from django.http import HttpResponse
import openpyxl
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Empleado, Prestamo, Cuota, TipoPrestamo, Comuna
from .forms import EmpleadoForm, PrestamoForm
from .serializers import EmpleadoSerializer, PrestamoSerializer, CuotaSerializer, TipoPrestamoSerializer, ComunaSerializer
from .services import generar_cuotas


@login_required
def dashboard(request):
    total_empleados    = Empleado.objects.count()
    total_prestamos    = Prestamo.objects.filter(estado=Prestamo.APROBADO).count()
    monto_total        = Prestamo.objects.filter(estado=Prestamo.APROBADO).aggregate(total=Sum('monto_prestamo'))['total'] or 0
    cuotas_vencidas    = Cuota.objects.filter(
        cuota_fecha_pago__isnull=True,
        cuota_fecha_vencimiento__lt=timezone.now()
    ).count()
    prestamos_pendientes = Prestamo.objects.filter(estado=Prestamo.PENDIENTE).count()

    pendientes_recientes = Prestamo.objects.filter(estado=Prestamo.PENDIENTE).order_by('-id_prestamo')[:5]

    return render(request, 'dashboard.html', {
        'total_empleados':      total_empleados,
        'total_prestamos':      total_prestamos,
        'monto_total':          monto_total,
        'cuotas_vencidas':      cuotas_vencidas,
        'prestamos_pendientes': prestamos_pendientes,
        'pendientes_recientes': pendientes_recientes,
    })


@login_required
def employee_list(request):
    qs = Empleado.objects.all().order_by('apellido_empleado', 'nombre_empleado')
    paginator = Paginator(qs, 10)
    empleados = paginator.get_page(request.GET.get('page'))
    return render(request, 'employee_list.html', {'empleados': empleados})


@login_required
def employee_create(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmpleadoForm()
    return render(request, 'employee_create.html', {'form': form})


@login_required
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


@login_required
def employee_delete(request, RUT_empleado):
    empleado = get_object_or_404(Empleado, RUT_empleado=RUT_empleado)
    empleado.delete()
    return redirect('employee_list')


@login_required
def loan_list(request):
    qs = Prestamo.objects.all().order_by('-id_prestamo')
    paginator = Paginator(qs, 10)
    prestamos = paginator.get_page(request.GET.get('page'))
    return render(request, 'loan_list.html', {'prestamos': prestamos})


@login_required
def loan_create(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loan_approvals')
    else:
        form = PrestamoForm()
    return render(request, 'loan_create.html', {'form': form})


@login_required
def loan_detail(request, id_prestamo):
    prestamo = get_object_or_404(Prestamo, id_prestamo=id_prestamo)
    cuotas = prestamo.cuotas.all()
    return render(request, 'loan_detail.html', {'prestamo': prestamo, 'cuotas': cuotas})


@login_required
def loan_approvals(request):
    pendientes = Prestamo.objects.filter(estado=Prestamo.PENDIENTE)
    return render(request, 'loan_approvals.html', {'pendientes': pendientes})


@login_required
def loan_approve(request, id_prestamo):
    prestamo = get_object_or_404(Prestamo, id_prestamo=id_prestamo)
    if prestamo.estado == Prestamo.PENDIENTE:
        prestamo.estado = Prestamo.APROBADO
        prestamo.save()
        generar_cuotas(prestamo)
    return redirect('loan_approvals')


@login_required
def loan_reject(request, id_prestamo):
    prestamo = get_object_or_404(Prestamo, id_prestamo=id_prestamo)
    if prestamo.estado == Prestamo.PENDIENTE:
        prestamo.estado = Prestamo.RECHAZADO
        prestamo.save()
    return redirect('loan_approvals')


@login_required
def cuota_pagar(request, id_cuota):
    cuota = get_object_or_404(Cuota, id_cuota=id_cuota)
    if not cuota.cuota_fecha_pago:
        cuota.cuota_fecha_pago = timezone.now()
        cuota.save()
    return redirect('loan_detail', id_prestamo=cuota.Prestamo.id_prestamo)


@login_required
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


# ─── Exportación ─────────────────────────────────────────────────────────────

@login_required
def export_excel(request, id_prestamo):
    prestamo = get_object_or_404(Prestamo, id_prestamo=id_prestamo)
    cuotas = prestamo.cuotas.all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f'Préstamo {id_prestamo}'

    ws.append([f'Préstamo #{prestamo.id_prestamo} — {prestamo.Empleado}'])
    ws.append([f'Tipo: {prestamo.TipoPrestamo}  |  Monto: ${prestamo.monto_prestamo}  |  Total a pagar: ${prestamo.monto_pagar}'])
    ws.append([])
    ws.append(['N° Cuota', 'Monto', 'Fecha Vencimiento', 'Fecha Pago', 'Estado'])

    for cuota in cuotas:
        ws.append([
            cuota.numero_cuota,
            cuota.monto_cuota,
            cuota.cuota_fecha_vencimiento.strftime('%d/%m/%Y'),
            cuota.cuota_fecha_pago.strftime('%d/%m/%Y') if cuota.cuota_fecha_pago else 'Pendiente',
            cuota.estado,
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="prestamo_{id_prestamo}.xlsx"'
    wb.save(response)
    return response


@login_required
def export_pdf(request, id_prestamo):
    prestamo = get_object_or_404(Prestamo, id_prestamo=id_prestamo)
    cuotas = prestamo.cuotas.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="prestamo_{id_prestamo}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph(f'Préstamo #{prestamo.id_prestamo} — {prestamo.Empleado}', styles['Title']))
    elementos.append(Paragraph(f'Tipo: {prestamo.TipoPrestamo} | Monto: ${prestamo.monto_prestamo} | Total a pagar: ${prestamo.monto_pagar}', styles['Normal']))

    datos = [['N° Cuota', 'Monto', 'Vencimiento', 'Fecha Pago', 'Estado']]
    for cuota in cuotas:
        datos.append([
            str(cuota.numero_cuota),
            f'${cuota.monto_cuota}',
            cuota.cuota_fecha_vencimiento.strftime('%d/%m/%Y'),
            cuota.cuota_fecha_pago.strftime('%d/%m/%Y') if cuota.cuota_fecha_pago else 'Pendiente',
            cuota.estado,
        ])

    tabla = Table(datos)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR',  (0, 0), (-1, 0), colors.white),
        ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    elementos.append(tabla)
    doc.build(elementos)
    return response
