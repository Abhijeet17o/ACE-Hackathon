from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import video, image, gemini

app = FastAPI()

origins = ["http://localhost:3000", "https://your-nextjs-frontend.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video.router, prefix="/video", tags=["Video"])
app.include_router(image.router, prefix="/image", tags=["Image"])
app.include_router(gemini.router, prefix="/gemini", tags=["Gemini"])
