from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.pdf_service import extract_text_from_pdf
from app.services.ai_service import analyze_scanned_document

router = APIRouter(prefix="/documents", tags=["Documents"])

MAX_FILES = 5
MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


@router.post("/upload")
async def upload_documents( files: list[UploadFile] = File(...)):
    if len(files) > MAX_FILES:
        raise HTTPException( status_code=400,
            detail="You can upload a maximum of 5 files.")

    results = []

    for file in files:

        if not file.filename:
            raise HTTPException( status_code=400,
                detail="A file is missing a filename."
            )

        contents = await file.read()

        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException( status_code=400,
                detail=f"{file.filename} exceeds the 10 MB limit."
            )

        if file.content_type == "application/pdf":

            text = extract_text_from_pdf(contents)

            results.append(
                {"filename": file.filename,
                "type": "pdf",
                "size_bytes": len(contents),
                "extracted_text_length": len(text),
                "text_preview": text[:200]}
                )

        elif file.content_type in ALLOWED_IMAGE_TYPES:

            text = await analyze_scanned_document(
                file_bytes=contents,
                mime_type=file.content_type
            )

            results.append(
                {"filename": file.filename,
                "type": "image",
                "size_bytes": len(contents),
                "extracted_text_length": len(text),
                "text_preview": text[:200]}
                )

        else:
            raise HTTPException(
                status_code=400,
                detail=f"{file.filename} is not a supported file type."
            )

    return {
        "number_of_files": len(results),
        "documents": results
    }