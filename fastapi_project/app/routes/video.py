from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import StreamingResponse
from app.services.mochi_api import generate_video_from_mochi
from io import BytesIO

router = APIRouter()

@router.post("/generate")
async def generate_video(script: str = Form(...)):
    try:
        video_content = generate_video_from_mochi(script)
        video_stream = BytesIO(video_content)
        return StreamingResponse(video_stream, media_type="video/mp4")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
