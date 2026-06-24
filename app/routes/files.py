from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os, uuid 
from .. import converters

router = APIRouter()


# ensure folders exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)


# -------------------------
# PDF → DOCX
# -------------------------
@router.post("/pdf-to-docx/")
async def pdf_to_docx(file: UploadFile = File(...)):

    name, ext = os.path.splitext(file.filename)

    if ext.lower() != ".pdf":
        return {"error": "File must be a PDF"}

    unique_name = f"{uuid.uuid4()}_{file.filename}"
    input_path = f"uploads/{unique_name}"
    output_path = f"outputs/{uuid.uuid4()}.pdf"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    converters.pdf_to_docx(input_path, output_path)

    return {
        "message": "PDF converted to DOCX",
        "download": f"/download/{name}.docx"
    }


# -------------------------
# DOCX → PDF
# -------------------------
@router.post("/docx-to-pdf/")
async def docx_to_pdf(file: UploadFile = File(...)):

    name, ext = os.path.splitext(file.filename)

    if ext.lower() != ".docx":
        return {"error": "File must be a DOCX"}

    unique_name = f"{uuid.uuid4()}_{file.filename}"
    input_path = f"uploads/{unique_name}"
    output_path = f"outputs/{uuid.uuid4()}.pdf"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    converters.docx_to_pdf(input_path, output_path)

    return {
        "message": "DOCX converted to PDF",
        "download": f"/download/{name}.pdf"
    }


# -------------------------
# IMAGE → PDF
# -------------------------
@router.post("/image-to-pdf/")
async def image_to_pdf(file: UploadFile = File(...)):

    name, ext = os.path.splitext(file.filename)

    allowed = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp", ".gif")

    if ext.lower() not in allowed:
        return {"error": "Unsupported image format"}

    unique_name = f"{uuid.uuid4()}_{file.filename}"
    input_path = f"uploads/{unique_name}"
    output_path = f"outputs/{uuid.uuid4()}.pdf"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    try:
        converters.image_to_pdf(input_path, output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if not os.path.exists(output_path):
     raise HTTPException(status_code=500, detail="Conversion failed")
    
    filename = os.path.basename(output_path)

    return {
    "success": True,
    "message": "Image converted to PDF",
    "filename": filename,
    "download_url": f"/download/{filename}"
}


# -------------------------
# DOWNLOAD FILE
# -------------------------
@router.get("/download/{filename}")
def download_file(filename: str):

    path = os.path.join("outputs", filename)

    if not os.path.exists(path):
        return {"error": f"{filename} was not created"}

    return FileResponse(path, filename=filename)

# -------------------------
# LIST FILES (for dropdown)
# -------------------------
@router.get("/files")
def list_files():

    files = os.listdir("outputs")

    return {"files": files}

# -------------------------
# MERGE PDFS
# -------------------------
@router.post("/merge-pdfs/")
async def merge_pdfs(files: list[UploadFile] = File(...)):

    input_paths = []

    for file in files:

        if not file.filename.lower().endswith(".pdf"):
            return {"error": "All files must be PDFs"}

        unique_name = f"{uuid.uuid4()}_{file.filename}"
        input_path = f"uploads/{unique_name}"

        with open(input_path, "wb") as f:
            f.write(await file.read())

        input_paths.append(input_path)

    output_filename = f"merged_{uuid.uuid4()}.pdf"
    output_path = f"outputs/{output_filename}"

    converters.merge_pdfs(input_paths, output_path)

    return {
        "message": "PDFs merged successfully",
        "filename": output_filename,
        "download_url": f"/download/{output_filename}"
    }