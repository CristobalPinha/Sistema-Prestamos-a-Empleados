
from django import forms
from .models import Comuna, Empleado, TipoPrestamo, Prestamo


#Crear Forms aqui
#===== Formulario para empleado =====

class ComunaForms(forms.ModelForm):
    class Meta:
        model = Comuna
        fields = ['id_comuna', 'nombre_comuna']

class EmpleadoForm(forms.ModelForm):
    Comuna  = forms.ModelChoiceField(queryset=Comuna.objects.all(), empty_label="Seleccione una comuna")
    class Meta:
        model = Empleado
        fields = ['RUT_empleado', 'nombre_empleado', 'apellido_empleado', 'direccion_empleado', 'Comuna']

#===== Formulario pare prestamos =====

class PrestamoForm(forms.ModelForm):
    Empleado = forms.ModelChoiceField(queryset=Empleado.objects.all(), empty_label="Seleccione un empleado",)
    TipoPrestamo = forms.ModelChoiceField(queryset=TipoPrestamo.objects.all(), empty_label="Seleccione el tipo de préstamo",)

    class Meta:
        model = Prestamo
        fields = [ 'id_prestamo', 'Empleado', 'TipoPrestamo', 'monto_prestamo', 'cantidad_cuotas']

