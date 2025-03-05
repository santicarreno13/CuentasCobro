from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)
CORS(app)

def generate_invoice(data):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Helvetica", 12)
    
    pdf.drawString(100, 750, "CORTINAS Y PERSIANAS LUCHO")
    pdf.drawString(100, 735, f"NIT-{data['empresa_nit']}")
    pdf.drawString(100, 720, f"BOGOTÁ {data['fecha']}")
    
    pdf.drawString(100, 690, "Señor(a):")
    pdf.drawString(100, 675, f"{data['cliente']}")
    pdf.drawString(100, 660, f"NIT: {data['cliente_nit']}")
    
    pdf.drawString(100, 630, "CUENTA DE COBRO")
    pdf.drawString(100, 600, "Por medio de la presente, me permito solicitar el pago correspondiente a:")
    pdf.drawString(100, 585, data['descripcion'])
    
    pdf.drawString(100, 560, f"Valor total: {data['valor_total']}")
    pdf.drawString(100, 545, f"Abono recibido: {data['abono']}")
    pdf.drawString(100, 530, f"Saldo pendiente: {data['saldo']}")
    
    pdf.drawString(100, 500, "Condiciones de pago:")
    pdf.drawString(100, 485, data['condiciones'])
    
    pdf.drawString(100, 450, "Atentamente:")
    pdf.drawString(100, 435, f"{data['remitente']}")
    pdf.drawString(100, 420, f"Cédula: {data['cedula_remitente']}")
    pdf.drawString(100, 405, f"Celular: {data['celular_remitente']}")
    
    pdf.save()
    buffer.seek(0)
    return buffer

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    pdf_file = generate_invoice(data)
    return send_file(pdf_file, as_attachment=True, download_name="Cuenta_de_Cobro.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)