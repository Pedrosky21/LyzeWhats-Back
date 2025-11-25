from fastapi import APIRouter, UploadFile, File
from app.services.whatsapp_parser import parse_whatsapp_chat
from app.services.analysis_service import analyze_chat

router = APIRouter()

@router.post("/upload")
async def upload_chat(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")

    messages = parse_whatsapp_chat(text)
    results = analyze_chat(messages)

    return {
        "status": "ok",
        "messages": len(messages),
        "analysis": results,
    }
