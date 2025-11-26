from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.upload_router import router as upload_router

origins = [
    "https://lyze-whats.vercel.app",
    "https://lyzewhats-back.onrender.com"
]

app = FastAPI(title="LyzeWhats API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/api")
