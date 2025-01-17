from huggingface_hub import InferenceClient
import os

# Load API key from environment variables
image_api_key = os.getenv("IMAGE_API_KEY")
model_name = "black-forest-labs/FLUX.1-dev"

def generate_image(prompt):
    """
    Generate an image using Hugging Face's FLUX model.

    Args:
        prompt (str): The text prompt for generating the image.

    Returns:
        Image: The generated image object.
    """
    if not image_api_key:
        raise ValueError("API key for image generation is missing.")

    client = InferenceClient(model_name, token=image_api_key)
    image = client.text_to_image(prompt)
    return image

def optimize_prompt_for_marketing(product_description, image_style, target_audience, call_to_action):
    """
    Create an optimized prompt tailored for marketing campaigns.

    Args:
        product_description (str): Product description.
        image_style (str): Desired image style.
        target_audience (str): Description of the target audience.
        call_to_action (str): Key message or visual emphasis.

    Returns:
        str: Optimized prompt.
    """
    return (
        f"Create a marketing campaign image for the product: '{product_description}'. "
        f"The image should have a {image_style} style, specifically designed to appeal to {target_audience}. "
        f"Include a strong call to action emphasizing {call_to_action}, with visuals that highlight the product's value."
    )
