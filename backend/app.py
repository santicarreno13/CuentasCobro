from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import io
import os

def draw_wrapped_text(pdf, text, x, y, max_width):
    """
    Función para dividir y dibujar texto en múltiples líneas dentro de un ancho máximo.
    """
    lines = simpleSplit(text, pdf._fontname, pdf._fontsize, max_width)
    for line in lines:
        pdf.drawString(x, y, line)
        y -= 15  # Ajusta el espaciado entre líneas
    return y  # Devuelve la última posición usada

def generate_invoice(data):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter  # Tamaño de la página

    # Ajustes generales de espaciado
    header_top_margin = 80
    footer_bottom_margin = 80

    # **Encabezado fijo con más margen superior**
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(width / 2, height - header_top_margin, "CORTINAS Y PERSIANAS LUCHO")
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(width / 2, height - header_top_margin - 20, f"NIT-{data['empresa_nit']}")
    
    # Ajustar posición de la fecha con más espaciado
    date_y = height - header_top_margin - 80  # Baja un poco la fecha
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(width / 2, date_y, f"BOGOTÁ, {data['fecha']}")
    
    # **Mayor espacio entre la fecha y el destinatario**
    y_position = date_y - 40
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, y_position, "Señor(a):")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(170, y_position, f"{data['cliente']}")
    pdf.drawString(100, y_position - 15, f"NIT: {data['cliente_nit']}")
    
    y_position -= 50  # Espaciado antes del título

    # **Título de la cuenta de cobro**
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(width / 2, y_position, "CUENTA DE COBRO")
    
    y_position -= 40  # Espaciado antes de la descripción

    # **Descripción del cobro con ajuste automático**
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, y_position, "Por medio de la presente, me permito solicitar el pago correspondiente a:")
    y_position -= 20  # Espaciado después del título
    y_position = draw_wrapped_text(pdf, data['descripcion'], 100, y_position, 400)  # Ajusta ancho de línea
    
    y_position -= 40  # Espaciado antes de los valores

    # **Detalles del pago**
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, y_position, "Valor total:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(200, y_position, f"${int(data['valor_total']):,}")
    
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, y_position - 15, "Abono recibido:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(200, y_position - 15, f"${int(data['abono']):,}")
    
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, y_position - 30, "Saldo pendiente:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(200, y_position - 30, f"${int(data['saldo']):,}")
    
    y_position -= 70  # Espaciado antes de condiciones

    # **Condiciones de pago con ajuste automático**
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, y_position, "Condiciones de pago:")
    y_position -= 20  # Espaciado antes del contenido

    pdf.setFont("Helvetica", 12)
    texto_fijo = ("Las persianas se entregan completamente instaladas y cuentan con "
                "garantía de un año. El pago se divide en un 50% de anticipo y el restante "
                "50% al recibir el producto. El tiempo estimado de fabricación e instalación "
                "es de cinco días hábiles.")

    # Dibujar el texto fijo de condiciones de pago
    y_position = draw_wrapped_text(pdf, texto_fijo, 100, y_position, 400)  
    y_position -= 15  # Espaciado antes del material seleccionado

    # **Dibujar el material seleccionado**
    pdf.setFont("Helvetica", 12)
    material_texto = f"El material seleccionado es {data['material']}."
    y_position = draw_wrapped_text(pdf, material_texto, 100, y_position, 400)  
    
    # **Pie de página más grande y con más margen inferior**
    footer_y = footer_bottom_margin + 30
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(width / 2, footer_y, "Atentamente")
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(width / 2, footer_y - 20, "Luis Antonio Carreño Gonzales")
    pdf.drawCentredString(width / 2, footer_y - 35, "Cc 79864703")
    pdf.drawCentredString(width / 2, footer_y - 50, "Cel. 3125915013")
    
    pdf.save()
    buffer.seek(0)
    return buffer

app = Flask(__name__)
CORS(app)

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    pdf_file = generate_invoice(data)
    return send_file(pdf_file, as_attachment=True, download_name="Cuenta_de_Cobro.pdf", mimetype='application/pdf')

# if __name__ == '__main__':
#     app.run(debug=True) # Descomentar para probar en local

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
