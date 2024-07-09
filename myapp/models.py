from django.db import models

# Crea tus modelos aqui

#============================================================================================================
#Tablas

class Comuna(models.Model):
    id_comuna = models.AutoField(primary_key=True)
    nombre_comuna = models.CharField(max_length= 50)
    def __str__(self):
        return self.nombre_comuna

class Empleado(models.Model):
    RUT_empleado = models.CharField(max_length=20, primary_key=True)
    nombre_empleado = models.CharField(max_length=50)
    apellido_empleado = models.CharField(max_length=50)
    direccion_empleado = models.CharField(max_length=100)
    Comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.nombre_empleado} {self.apellido_empleado}'

class TipoPrestamo(models.Model):
    id_tipo_prestamo = models.AutoField(primary_key=True)
    tipo_prestamo = models.CharField(max_length=50)
    tasa_de_interes = models.IntegerField()  
    
    def __str__(self):
        return self.tipo_prestamo

class Prestamo(models.Model):
    id_prestamo = models.AutoField(primary_key=True)
    monto_prestamo = models.IntegerField()
    monto_pagar = models.IntegerField(blank=True, null=True)  # Para mostrar el monto total a pagar
    Empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, to_field='RUT_empleado')  # La relación ya está correctamente definida
    TipoPrestamo = models.ForeignKey(TipoPrestamo, on_delete=models.CASCADE)
    cantidad_cuotas = models.IntegerField()  # En plural

    def save(self, *args, **kwargs):
        if not self.monto_pagar:  # Calcular solo si monto_pagar no está definido
            tasa_interes_decimal = self.TipoPrestamo.tasa_de_interes / 100.0
            self.monto_pagar = self.monto_prestamo + (self.monto_prestamo * tasa_interes_decimal)
        super().save(*args, **kwargs)
    
class Cuota(models.Model):
    id_cuota = models.AutoField(primary_key=True)
    Prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE, related_name='cuotas')
    numero_cuota = models.IntegerField()
    monto_cuota = models.IntegerField()
    cuota_fecha_emision = models.DateTimeField(auto_now_add=True)  # Fecha de emisión de la cuota
    cuota_fecha_vencimiento = models.DateTimeField()
    cuota_fecha_pago = models.DateTimeField(null=True, blank=True)  # Puede ser nulo si no ha sido pagada aún
    
    def __str__(self):
        return f'Cuota {self.numero_cuota} - Préstamo {self.Prestamo.id_prestamo}'
#============================================================================================================