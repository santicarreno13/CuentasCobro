from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io

def generate_invoice(data):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter  # Tamaño de la página

    # Ajustes generales de espaciado
    header_top_margin = 80
    content_start_y = height - 160
    footer_bottom_margin = 80

    # **Encabezado fijo con más margen superior**
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(width / 2, height - header_top_margin, "CORTINAS Y PERSIANAS LUCHO")
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(width / 2, height - header_top_margin - 20, f"NIT-{data['empresa_nit']}")
    
    # Ajustar posición de la fecha con más espaciado
    date_y = height - header_top_margin - 80  # Baja un poco la fecha
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(width / 2, date_y, f"BOGOTÁ, {data['fecha']}")

    
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

    # **Descripción del cobro**
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, y_position, "Por medio de la presente, me permito solicitar el pago correspondiente a:")
    y_position -= 15
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, y_position, data['descripcion'])
    
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

    # **Condiciones de pago**
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, y_position, "Condiciones de pago:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, y_position - 15, data['condiciones'])
    
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
    app.run(host='0.0.0.0', port=10000, debug=True)
