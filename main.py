from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

app = Flask(__name__)
CORS(app)  # Enable CORS to allow your frontend to call this API

# Health check route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "✅ Meesho API is live"})

# /process route which accepts PDF file uploads and processes them
@app.route("/process", methods=["POST"])
def process_pdf():
    file = request.files.get("pdf")
    if not file or not file.filename.endswith(".pdf"):
        return "Invalid file", 400

    try:
        reader = PdfReader(file)
        writer = PdfWriter()

        # Example: Crop each page to keep only the top half.
        # (You can update the logic here to crop above "TAX INVOICE" or more refined process.)
        for page in reader.pages:
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            # For demonstration, keep only the top half:
            page.mediabox.upper_right = (width, height / 2)
            writer.add_page(page)

        output = BytesIO()
        writer.write(output)
        output.seek(0)
        return send_file(
            output,
            as_attachment=True,
            download_name="cropped_labels.pdf",
            mimetype="application/pdf"
        )
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(debug=True)
