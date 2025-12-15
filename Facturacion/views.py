from django.shortcuts import render, redirect, get_object_or_404
from .models import Cita, Ingreso, Factura, Paciente
from .serializers import CitaSerializer, IngresoSerializer, FacturaSerializer
from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Cita, Ingreso, Factura, Doctor, Especialidad, Habitacion
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .emailutils import generar_factura_pdf_buffer, enviar_factura_por_email_con_adjunto

class CitaViewSet(viewsets.ModelViewSet):
    serializer_class = CitaSerializer
    

    def get_queryset(self):
        return Cita.objects.filter(publicado=True)
    

    @action(detail=False, methods=['get'])
    def citas_generales(self, request):
        doctor = request.user.doctor
        Citas = Cita.objects.filter(doctor=doctor)
        serializer = self.get_serializer(Citas, many=True)
        return Response(serializer.data)

class IngresoViewSet(viewsets.ModelViewSet):
    serializer_class = IngresoSerializer
    

    def get_queryset(self):
        return Ingreso.objects.filter(paciente__usuario=self.request.user)



class FacturaViewSet(viewsets.ModelViewSet):
    serializer_class = FacturaSerializer
    
    # 1. Permite acceso total para cualquier operación (GET, POST, PUT, DELETE)
    permission_classes = [permissions.AllowAny] 
    
    def get_queryset(self):
        # 2. Permite ver TODAS las facturas para cualquier GET request
        return Factura.objects.all()

 # Añade el decorador para asegurar que haya un usuario
def cliente_dashboard(request):
    paciente_prueba = Paciente.objects.get(cedula='12345678') # Cambia esto por una cédula existente

    citas = Cita.objects.filter(paciente=paciente_prueba)
    ingresos = Ingreso.objects.filter(paciente=paciente_prueba)
    facturas = Factura.objects.filter(paciente=paciente_prueba)

    contexto = {
        'citas': citas,
        'ingresos': ingresos,
        'facturas': facturas,
        # Necesitas pasar los datos para los Modales
        'especialidades': Especialidad.objects.all(),
        'doctores': Doctor.objects.all(),
        'habitaciones': Habitacion.objects.filter(disponible=True) # O el filtro que uses
    }
    return render(request, 'Cliente/ClienteDashboard.html', contexto)


def crear_cita(request):
    if request.method == "POST":
        paciente = request.user.paciente
        doctor_id = request.POST.get("doctor")
        especialidad_id = request.POST.get("especialidad")
        fecha_hora = request.POST.get("fecha_hora")
        motivo = request.POST.get("motivo")

        doctor = Doctor.objects.get(id=doctor_id)
        especialidad = Especialidad.objects.get(id=especialidad_id)

        Cita.objects.create(
            paciente=paciente,
            doctor=doctor,
            Especialidad=especialidad,
            fecha_hora=fecha_hora,
            motivo=motivo
        )
    return redirect('cliente_dashboard')  # Redirige al dashboard


def crear_ingreso(request):
    if request.method == "POST":
        paciente = request.user.paciente
        habitacion_id = request.POST.get("habitacion")
        doctor_id = request.POST.get("doctor")
        motivo = request.POST.get("motivo")

        habitacion = Habitacion.objects.get(id=habitacion_id)
        doctor = Doctor.objects.get(id=doctor_id)

        Ingreso.objects.create(
            paciente=paciente,
            habitacion=habitacion,
            fecha_ingreso=timezone.now(),  # o puedes usar un input si quieres
            doctor_tratante=doctor,
            motivo=motivo
        )
    return redirect('cliente_dashboard')


# vistas.py (Facturación)


def descargar_factura(request, factura_id):
    """
    Genera el PDF de la factura y lo descarga directamente, accesible por cualquiera.
    """
    factura = get_object_or_404(Factura, pk=factura_id)
    
    # 1. SEGURIDAD: VERIFICACIÓN DEL DUEÑO ELIMINADA. 
    # Cualquier usuario puede descargar la factura si conoce el ID.
    
    # 2. Generar el PDF buffer
    pdf_buffer = generar_factura_pdf_buffer(factura=factura)

    # 3. Crear la respuesta HTTP de descarga
    # Manejar el caso si el paciente no tiene cédula (opcional)
    cedula = factura.paciente.cedula if factura.paciente and factura.paciente.cedula else 'SINCEDULA' 
    
    response = HttpResponse(pdf_buffer, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="factura_{factura.id}_{cedula}.pdf"'
    return response

# vistas.py (Facturación)

# NOTA: ELIMINAR el decorador @login_required si estaba presente aquí.

def enviar_factura_view(request, factura_id):
    """
    Genera el PDF y lo envía por correo. Se requiere que el email de destino 
    sea proporcionado por POST si el usuario no está logueado.
    """
    factura = get_object_or_404(Factura, pk=factura_id)

    # 1. SEGURIDAD: VERIFICACIÓN DEL DUEÑO ELIMINADA.

    # 2. Determinar el correo de destino
    correo_destino = None
    
    # Si la petición es POST, el email DEBE venir en el formulario
    if request.method == "POST":
        correo_destino = request.POST.get("email_destino")
    
    # Si la petición no es POST o si el email_destino no se encontró,
    # y el usuario está logueado, usar el email del usuario.
    elif request.user.is_authenticated:
        correo_destino = request.user.email
    
    # Si no se pudo determinar el destino (ej. usuario anónimo sin POST data)
    if not correo_destino:
        messages.error(request, 'Debes proporcionar un email de destino válido.')
        # Redirigir a una URL segura si falta información
        return HttpResponseRedirect(reverse("cliente_dashboard"))

    # 3. Generar el PDF buffer
    pdf_buffer = generar_factura_pdf_buffer(factura=factura)
    
    # 4. Enviar el correo con el PDF adjunto
    if enviar_factura_por_email_con_adjunto(
        factura=factura,
        pdf_buffer=pdf_buffer,
        correo_destino=correo_destino
    ):
        messages.success(request, f"Factura N° {factura.id} enviada a {correo_destino} correctamente.")
    else:
        messages.error(request, 'Hubo un error al enviar el correo. Verifica el destinatario y la configuración de email.')

    # Redirigir al dashboard
    return HttpResponseRedirect(reverse("cliente_dashboard"))