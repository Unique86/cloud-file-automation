# app/converters.py
from pdf2docx import Converter
from PIL import Image
from PyPDF2 import PdfMerger
from docx import Document
import os
import subprocess

# PDF → DOCX
def pdf_to_docx(input_path, output_path):
    cv = Converter(input_path)
    cv.convert(output_path)
    cv.close()

# DOCX → PDF
# (example using python-docx + reportlab or any method you used)
def docx_to_pdf(input_path, output_path):
    output_dir = os.path.dirname(output_path)

    subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            output_dir,
            input_path,
        ],
        check=True,
    )


# Image → PDF
def image_to_pdf(input_path, output_path):
    try:
        image = Image.open(input_path)

        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        image.save(output_path, "PDF")

    except Exception as e:
        raise RuntimeError(f"Image conversion failed: {str(e)}")
        




# Merge PDFs
def merge_pdfs(file_paths, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    merger = PdfMerger()
    for path in file_paths:
        merger.append(path)
    merger.write(output_path)
    merger.close()
