from django.core.mail import EmailMessage
from django.conf import settings
# 🚨 DEBES CREAR LA FUNCIÓN 'generar_factura_pdf'
from .pdf_generator import generar_factura_pdf_buffer
from io import BytesIO 

def enviar_factura_por_email_con_adjunto(factura, pdf_buffer, correo_destino=None):
    """
    Envía el PDF de Factura ya generado por correo electrónico.
    """
    
    # 1. Prepara el correo
    nombre_paciente = factura.paciente.nombre
    
    # Usar el correo proporcionado o el correo del paciente por defecto
    email_destino = correo_destino if correo_destino else factura.paciente.usuario.email
    
    asunto = f"Factura N° {factura.id} - Hospital Moderno"
    cuerpo = (
        f"Estimado/a {nombre_paciente},\n\n"
        f"Adjuntamos su Factura N° {factura.id} en PDF por el monto total de ${factura.total}.\n"
        f"El archivo está protegido con su número de cédula/identificación.\n\n"
        "Gracias por su preferencia."
    )

    email = EmailMessage(
        subject=asunto,
        body=cuerpo,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email_destino],
    )
    
    # Resetear la posición del buffer antes de adjuntar
    pdf_buffer.seek(0)
    pdf_bytes = pdf_buffer.read()

    # 2. Adjunta el PDF
    email.attach(
        filename=f"factura_{factura.id}.pdf",
        content=pdf_bytes,
        mimetype="application/pdf",
    )
    
    # 3. Envía el correo
    try:
        email.send()
        print(f"FACTURA {factura.id} ENVIADA A: {email_destino}")
        return True
    except Exception as e:
        print(f"ERROR ENVIANDO FACTURA {factura.id}: {repr(e)}")
        return False

# Mantenemos esta función para la lógica que solo necesita el objeto
def generar_factura_pdf(factura):
    """ Función que envuelve a pdf_generator.generar_factura_pdf """
    # Nota: Asegúrate de que esta función esté implementada y llama a tu PDFGenerador
    return generar_factura_pdf_buffer(factura=factura)