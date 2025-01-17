from fastapi import APIRouter, HTTPException, Form
from app.services.gemini_api import process_input_with_gemini, extract_details_from_gemini_response, fetch_youtube_channels
import json

router = APIRouter()

@router.post("/generate")
async def generate_product_info(statement: str = Form(...)):
    try:
        input_text = (
            f"Given the product description: '{statement}', identify relevant categories and the target age group.\n\n"
            "Respond in this exact format:\n\n"
            "Categories: category1, category2\n"
            "Age Group: age_group"
        )

        response = process_input_with_gemini(input_text)
        categories, age_group = extract_details_from_gemini_response(response)
        account_names = fetch_youtube_channels(categories)

        output_data = {
            'Categories': categories,
            'Age Group': age_group,
            'Channels': account_names
        }

        return output_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
