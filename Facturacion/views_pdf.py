from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .emailutils import generar_factura_pdf_buffer, enviar_factura_por_email_con_adjunto
from .models import Factura, Paciente # Asegúrate de que Factura y Paciente sean accesibles (si están en otro archivo de models)


# --- 1. FUNCIÓN ADAPTADA: DESCARGAR FACTURA (análoga a descargar_certificado) ---


def descargar_factura(request, factura_id):
    """
    Genera el PDF encriptado de la factura especificada y lo fuerza a la descarga.
    """
    # Intentamos obtener la factura que pertenece al ID
    factura = get_object_or_404(Factura, pk=factura_id)
    
    # 1. SEGURIDAD: Verificar que el paciente logueado es el dueño de la factura
    try:
        if factura.paciente != request.user.paciente:
            messages.error(request, 'No tienes permiso para descargar esta factura.')
            # Asumiendo que 'cliente_dashboard' es tu vista principal de cliente
            return HttpResponseRedirect(reverse("cliente_dashboard")) 
    except Paciente.DoesNotExist:
        messages.error(request, 'Error de autenticación del paciente.')
        return HttpResponseRedirect(reverse("cliente_dashboard"))
        
    # 2. Generar el PDF buffer (esto devuelve un objeto BytesIO encriptado)
    pdf_buffer = generar_factura_pdf_buffer(factura=factura)

    # 3. Preparar la respuesta HTTP para la descarga
    cedula = factura.paciente.cedula 
    
    # Usamos .getvalue() para obtener el contenido del BytesIO
    response = HttpResponse(pdf_buffer.getvalue(), content_type="application/pdf")
    
    # Establecer el nombre del archivo para la descarga
    response["Content-Disposition"] = f'attachment; filename="factura_{factura.id}_PROTEGIDA.pdf"'
    
    return response


# --- 2. FUNCIÓN ADAPTADA: ENVIAR FACTURA POR CORREO (análoga a enviar_certificado_view) ---


def enviar_factura_view(request, factura_id):
    """
    Genera el PDF de la factura y lo envía por correo electrónico al destinatario.
    """
    factura = get_object_or_404(Factura, pk=factura_id)

    # 1. SEGURIDAD: Verificar dueño
    try:
        if factura.paciente != request.user.paciente:
            messages.error(request, 'No tienes permiso para enviar esta factura.')
            return HttpResponseRedirect(reverse("cliente_dashboard"))
    except Paciente.DoesNotExist:
        messages.error(request, 'Error de autenticación del paciente.')
        return HttpResponseRedirect(reverse("cliente_dashboard"))

    # 2. Determinar el correo de destino
    correo_destino = request.user.email
    if request.method == "POST":
        # Se asume que en el POST puede venir un campo 'email_destino'
        correo_destino = request.POST.get("email_destino", request.user.email)
    
    # 3. Generar el PDF buffer
    pdf_buffer = generar_factura_pdf_buffer(factura=factura)
    
    # 4. Enviar el correo con el PDF adjunto (usa la función de utils)
    if enviar_factura_por_email_con_adjunto(
        factura=factura,
        pdf_buffer=pdf_buffer,
        correo_destino=correo_destino
    ):
        messages.success(request, f"Factura N° {factura.id} enviada a {correo_destino} correctamente.")
    else:
        messages.error(request, 'Hubo un error al enviar el correo. Verifique la configuración de email.')

    # Redirigir al dashboard
    return HttpResponseRedirect(reverse("cliente_dashboard"))