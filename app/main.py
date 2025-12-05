from fastapi import FastAPI
from app.api.routers.eligibility_router import router as eligibility_router

app = FastAPI(title="ProtocolIQ Parser Service")

app.include_router(eligibility_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}
