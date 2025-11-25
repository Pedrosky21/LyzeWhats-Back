from fastapi import FastAPI
from app.routers.upload_router import router as upload_router

app = FastAPI(title="LyzeWhats API")

app.include_router(upload_router, prefix="/api")
