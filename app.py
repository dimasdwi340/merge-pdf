from flask import Flask, request, render_template, send_file, redirect, url_for
from PyPDF2 import PdfReader, PdfWriter
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Ambil file yang diunggah
        main_pdf = request.files.get("main_pdf")
        insert_pdf = request.files.get("insert_pdf")

        if not main_pdf or not insert_pdf:
            return "Pastikan kedua file PDF diunggah.", 400

        # Simpan file yang diunggah
        main_pdf_path = os.path.join(UPLOAD_FOLDER, main_pdf.filename)
        insert_pdf_path = os.path.join(UPLOAD_FOLDER, insert_pdf.filename)
        output_pdf_path = os.path.join(OUTPUT_FOLDER, "Cepat Rename File ini.pdf")

        main_pdf.save(main_pdf_path)
        insert_pdf.save(insert_pdf_path)

        # Proses penyisipan file PDF
        try:
            reader_main = PdfReader(main_pdf_path)
            reader_insert = PdfReader(insert_pdf_path)
            writer = PdfWriter()

            # Tambahkan halaman pertama dari file utama
            writer.add_page(reader_main.pages[0])

            # Tambahkan semua halaman dari file yang akan disisipkan
            for page in reader_insert.pages:
                writer.add_page(page)

            # Tambahkan sisa halaman dari file utama
            for page in reader_main.pages[1:]:
                writer.add_page(page)

            # Simpan output
            with open(output_pdf_path, "wb") as output_file:
                writer.write(output_file)

            # Kembalikan file hasil untuk diunduh
            return send_file(output_pdf_path, as_attachment=True)

        except Exception as e:
            return f"Terjadi kesalahan: {e}", 500

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
