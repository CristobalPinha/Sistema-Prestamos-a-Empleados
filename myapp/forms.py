
from django import forms
from .models import Comuna, Empleado, TipoPrestamo, Prestamo


def validar_rut(rut):
    """Valida formato y dígito verificador de un RUT chileno. Acepta puntos y guión."""
    # Normalizar: quitar puntos y espacios, pasar K a mayúscula
    rut = rut.replace('.', '').replace(' ', '').upper()

    # Verificar formato: dígitos + guión + (dígito o K)
    if '-' not in rut:
        raise forms.ValidationError('El RUT debe incluir guión (ej: 12345678-9).')

    cuerpo, dv_ingresado = rut.rsplit('-', 1)

    if not cuerpo.isdigit():
        raise forms.ValidationError('El RUT contiene caracteres inválidos.')

    if dv_ingresado not in [str(i) for i in range(10)] + ['K']:
        raise forms.ValidationError('El dígito verificador es inválido.')

    # Algoritmo Módulo 11
    suma = 0
    multiplicador = 2
    for digito in reversed(cuerpo):
        suma += int(digito) * multiplicador
        multiplicador = multiplicador + 1 if multiplicador < 7 else 2

    resto = suma % 11
    dv_calculado = 11 - resto
    if dv_calculado == 11:
        dv_esperado = '0'
    elif dv_calculado == 10:
        dv_esperado = 'K'
    else:
        dv_esperado = str(dv_calculado)

    if dv_ingresado != dv_esperado:
        raise forms.ValidationError(f'El dígito verificador es incorrecto (esperado: {dv_esperado}).')

    # Retornar el RUT normalizado (sin puntos, con guión)
    return f'{cuerpo}-{dv_ingresado}'


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

    def clean_RUT_empleado(self):
        rut = self.cleaned_data.get('RUT_empleado', '')
        return validar_rut(rut)

#===== Formulario pare prestamos =====

class PrestamoForm(forms.ModelForm):
    Empleado = forms.ModelChoiceField(queryset=Empleado.objects.all(), empty_label="Seleccione un empleado",)
    TipoPrestamo = forms.ModelChoiceField(queryset=TipoPrestamo.objects.all(), empty_label="Seleccione el tipo de préstamo",)

    class Meta:
        model = Prestamo
        fields = [ 'id_prestamo', 'Empleado', 'TipoPrestamo', 'monto_prestamo', 'cantidad_cuotas']

