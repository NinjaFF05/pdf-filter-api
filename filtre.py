from flask import Flask, request, send_file
from PyPDF2 import PdfReader, PdfWriter
import pdfplumber
import io

app = Flask(__name__)

@app.route("/")
def index():
    return "PDF Table Filter API is running!"

@app.route("/filter_pdf", methods=["POST"])
def filter_pdf():
    if 'file' not in request.files:
        return "Missing 'file' in request", 400

    file = request.files['file']
    pdf_bytes = file.read()

    reader = PdfReader(io.BytesIO(pdf_bytes))
    writer = PdfWriter()

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            tables = page.extract_tables()
            if tables and any(k in text.lower() for k in ["bilan", "actif", "passif"]):
                writer.add_page(reader.pages[i])

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)

    return send_file(output, download_name="filtered.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
