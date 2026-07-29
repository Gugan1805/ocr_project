from fastapi import FastAPI

from app.routes import ocr_router

app = FastAPI(
    title="OCR API",
    version="1.0.0",
)

app.include_router(ocr_router)