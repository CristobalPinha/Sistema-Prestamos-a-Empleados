from .models import Prestamo

def sidebar_context(request):
    return {
        'sidebar_pendientes': Prestamo.objects.filter(estado=Prestamo.PENDIENTE).count()
    }
