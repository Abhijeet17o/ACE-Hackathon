from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import FileResponse
from app.services.image_api import generate_image, optimize_prompt_for_marketing

router = APIRouter()

@router.post("/generate")
async def generate_marketing_image(
    product_description: str = Form(...),
    image_style: str = Form(...),
    target_audience: str = Form(...),
    call_to_action: str = Form(...)
):
    try:
        # Create the optimized prompt
        prompt = optimize_prompt_for_marketing(
            product_description, image_style, target_audience, call_to_action
        )
        # Generate the image
        image = generate_image(prompt)

        # Save the image to a file
        image_path = "generated_image.png"
        image.save(image_path, format="PNG")

        return FileResponse(image_path, media_type="image/png", filename="marketing_image.png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")
