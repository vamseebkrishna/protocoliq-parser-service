from fastapi import APIRouter, UploadFile, File
from app.application.pipelines.eligibility_pipeline import EligibilityPipeline

router = APIRouter()

@router.post("/parse/pdf")
async def parse_pdf(file: UploadFile = File(...)):
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    pipeline = EligibilityPipeline()
    result = pipeline.parse_pdf(temp_path)

    return result
