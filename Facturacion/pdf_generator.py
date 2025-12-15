from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from PyPDF2 import PdfWriter, PdfReader
from io import BytesIO
from datetime import datetime
import hashlib
import os
from .models import Factura, DetalleFactura, Paciente
import io
# ----------------------------------------------------------------------
# CLASE PDFGenerador (SIN CAMBIOS)
# ----------------------------------------------------------------------

class PDFGenerador:
    """Genera PDFs con contenido y encriptación con contraseña"""

    def __init__(self, titulo="Documento Hospital Moderno"):
        self.titulo = titulo
        self.styles = getSampleStyleSheet()
        self.pagesize = A4

    # ... (Todos los métodos: generar_pdf_con_encriptacion, _crear_tabla_datos, 
    # _crear_tabla, _encriptar_pdf se mantienen IGUALES) ...

    # Nota: Asegúrate de reemplazar "1234" por la cédula real en _encriptar_pdf
    def _encriptar_pdf(self, buffer_pdf, cedula=None):
        """
        Encripta el PDF con contraseña (basada en la cédula).
        """
        # Usaremos la cédula completa como contraseña
        contrasena = "1234"
        
        # Leer el PDF
        pdf_reader = PdfReader(buffer_pdf)
        pdf_writer = PdfWriter()

        # Agregar todas las páginas
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        # Encriptar 
        pdf_writer.encrypt(user_password=contrasena, owner_password=contrasena)

        output_buffer = BytesIO()
        pdf_writer.write(output_buffer)
        output_buffer.seek(0)
        return output_buffer
    
    def _generar_contenido_factura(self, factura):
        """Genera el contenido PDF usando ReportLab y devuelve el buffer NO encriptado."""
        
        # 1. Crear el buffer de memoria
        buffer = io.BytesIO()
        
        # 2. Configurar el documento
        doc = SimpleDocTemplate(buffer, pagesize=letter, # Usamos letter como en tu código
                                topMargin=50, bottomMargin=50,
                                leftMargin=50, rightMargin=50)
        
        styles = self.styles # Usamos los estilos inicializados en __init__
        elements = []
        
        # --- 3. Encabezado de la Factura ---
        elements.append(Paragraph(f"<b>FACTURA N° {factura.id}</b>", styles['Heading1']))
        elements.append(Spacer(1, 12))
        
        # Información de la Empresa/Hospital
        elements.append(Paragraph("<b>HOSPITAL EL BUEN SAMARITANO</b>", styles['Normal']))
        elements.append(Paragraph("Dirección: Calle Falsa 123 | Teléfono: 555-0199", styles['Normal']))
        elements.append(Paragraph(f"Fecha de Emisión: {factura.fecha_emision.strftime('%d/%m/%Y')}", styles['Normal']))
        elements.append(Spacer(1, 24))
        
        # --- 4. Información del Cliente/Paciente ---
        try:
            # Capturamos el email del paciente de forma segura
            paciente_email = factura.paciente.user.email if hasattr(factura.paciente, 'user') and factura.paciente.user else 'N/A'
        except Exception:
             paciente_email = 'N/A'
             
        paciente_info = [
            [Paragraph("<b>Información del Paciente</b>", styles['Heading3']), ''],
            [f"Nombre: {factura.paciente.nombre}", f"Cédula: {factura.paciente.cedula}"],
            [f"Email: {paciente_email}", f"Teléfono: {factura.paciente.telefono or 'N/A'}"],
        ]
        
        paciente_table = Table(paciente_info, colWidths=[250, 250])
        paciente_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ]))
        elements.append(paciente_table)
        elements.append(Spacer(1, 18))
        
        # --- 5. Detalle de los Ítems (Tabla) ---
        
        # Acceso a los detalles de la factura (usando la lógica de fallback)
        try:
            detalles = factura.detalles_factura.all() # Intenta el related_name
        except AttributeError:
            detalles = factura.detallefactura_set.all() # Usa el valor por defecto
            
        data = [
            ['Descripción', 'Cantidad', 'Precio Unitario', 'Subtotal']
        ]
        subtotal_general = 0
        
        for item in detalles:
            precio_unitario = item.precio 
            cantidad = item.cantidad
            subtotal = precio_unitario * cantidad
            subtotal_general += subtotal
            
            data.append([
                item.descripcion,
                cantidad,
                f"${precio_unitario:,.2f}",
                f"${subtotal:,.2f}"
            ])

        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        
        items_table = Table(data, colWidths=[200, 70, 110, 110])
        items_table.setStyle(table_style)
        elements.append(items_table)
        elements.append(Spacer(1, 18))
        
        # --- 6. Totales ---
        
        iva = subtotal_general * 0.16 # Ejemplo de IVA
        total_final = subtotal_general + iva
        
        total_data = [
            ['SUBTOTAL:', f"${subtotal_general:,.2f}"],
            ['IVA (16%):', f"${iva:,.2f}"],
            ['TOTAL A PAGAR:', f"${total_final:,.2f}"],
        ]
        
        # Tabla de totales alineada a la derecha
        total_table = Table(total_data, colWidths=[400, 110])
        total_table.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 2), (-1, 2), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(total_table)
        
        # --- 7. Construir y Cerrar ---
        doc.build(elements)
        
        # Importante: Mover el cursor al inicio del buffer antes de devolverlo
        buffer.seek(0)
        return buffer
        
    
    def generar_factura_con_encriptacion(self, factura):
        """
        Genera el contenido del PDF, lo encripta y devuelve el buffer encriptado.
        """
        # 1. Generar el PDF sin encriptar (usando la lógica de ReportLab)
        pdf_buffer_original = self._generar_contenido_factura(factura)
        
        # 2. Obtener la cédula/contraseña
        
        # 3. Encriptar y devolver el buffer protegido
        return self._encriptar_pdf(pdf_buffer_original)

    # --- Método que contiene la lógica de ReportLab (Tu código original) ---


# ----------------------------------------------------------------------
# FUNCIÓN ADAPTADA: generar_factura_pdf
# ----------------------------------------------------------------------

# 🚨 Asumimos que esta función será llamada desde tu utils.py 
# y que recibirá un objeto Factura de Django o datos pre-procesados.

