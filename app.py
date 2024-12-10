import os
from flask import Flask, request, render_template, send_file
from PyPDF2 import PdfReader, PdfWriter
import tempfile

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Buat folder sementara
        with tempfile.TemporaryDirectory() as temp_dir:
            # Simpan file yang diunggah ke folder sementara
            main_pdf = request.files.get("main_pdf")
            insert_pdf = request.files.get("insert_pdf")

            if not main_pdf or not insert_pdf:
                return "Pastikan kedua file PDF diunggah.", 400

            # Dapatkan nama file utama tanpa ekstensi
            main_pdf_name = os.path.splitext(main_pdf.filename)[0]
            combined_pdf_name = f"{main_pdf_name}_combined.pdf"

            # Simpan file sementara
            main_pdf_path = f"{temp_dir}/main.pdf"
            insert_pdf_path = f"{temp_dir}/insert.pdf"
            output_pdf_path = f"{temp_dir}/{combined_pdf_name}"

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

                # Kirim file hasil untuk diunduh
                return send_file(output_pdf_path, as_attachment=True, download_name=combined_pdf_name)

            except Exception as e:
                return f"Terjadi kesalahan: {e}", 500

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
