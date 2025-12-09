import os
from fastapi import APIRouter, UploadFile, File
from app.application.pipelines.eligibility_pipeline import EligibilityPipeline
import tempfile

router = APIRouter()



@router.post("/parse/pdf")
async def parse_pdf(file: UploadFile = File(...)):
    # Create a temporary file path in OS-safe location
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, file.filename)

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    pipeline = EligibilityPipeline()
    result = pipeline.parse_pdf(temp_path)

    return result
