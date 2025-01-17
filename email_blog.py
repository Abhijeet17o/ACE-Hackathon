import requests

# Set up Gemini API key
GEMINI_API_KEY = 'AIzaSyBKmt9XbcXlPDXV-x5z0edmSPWG0kOkctE'
GEMINI_TEXT_ENDPOINT = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}'

# Function to generate text content using Gemini
def generate_text(prompt):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    response = requests.post(GEMINI_TEXT_ENDPOINT, headers=headers, json=data)
    response.raise_for_status()
    
    # Print the response JSON for debugging
    response_json = response.json()
    print("Response JSON:", response_json)
    
    # Extract the generated text from the response
    if 'candidates' in response_json:
        return response_json['candidates'][0]['content']['parts'][0]['text']
    else:
        raise KeyError("'candidates' key not found in the response")

# # Function to format the generated text
# def format_text(text):
#     # Replace placeholder text with actual product details
#     formatted_text = text.replace("[Product Name]", "Your Product")
#     formatted_text = formatted_text.replace("[Problem]", "a common problem")
#     formatted_text = formatted_text.replace("[Benefit]", "a benefit")
#     formatted_text = formatted_text.replace("[Verb related to product use]", "use")
#     return formatted_text

# Generate email content
def generate_email_content(keywords: list[str], product: str):
    email_subject = generate_text(f"Generate a {keywords} email subject for our {product}.")
    email_body = generate_text(f"Generated an {keywords} email body for our {product}.")
    return {
        "subject": email_subject,
        "body": email_body
    }

# Generate blog content
def generate_blog_content(product: str):
    blog_idea = generate_text(f"Give me a list of 10 blog ideas related to the {product}")
    # blog_title = generate_text("Generate a blog title for our new shoes.")
    # blog_body = generate_text("Generate a detailed blog post about our new shoes.")
    return {
        "blog_ideas": blog_idea
    }

# Example usage
if __name__ == "__main__":
    try:
        email_content = generate_email_content(['catchy', 'exclusive','bold'], 'shoes called FLYERS')
        blog_content = generate_blog_content("shoes called FLYERS")
        
        print("Email Subject:")
        print(email_content['subject'])
        print("\nEmail Body:")
        print(email_content['body'])
        
        print("\nBlog Ideas:")
        print(blog_content['blog_ideas'])
        
    except Exception as e:
        print("An error occurred:", e)