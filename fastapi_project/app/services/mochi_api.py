import requests
from fastapi import HTTPException

# Mochi API details
api_key = "SG_137cdb30d6419a5a"
mochi_url = "https://api.segmind.com/v1/mochi-1"

def generate_video_from_mochi(script: str):
    data = {
        "prompt": script,
        "negative_prompt": "blurry, low quality, distorted",
        "guidance_scale": 4.5,
        "fps": 24,
        "steps": 30,
        "seed": 985521,
        "frames": 120,
    }
    headers = {"x-api-key": api_key}
    response = requests.post(mochi_url, json=data, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        raise HTTPException(
            status_code=response.status_code, detail=f"Error: {response.text}"
        )
