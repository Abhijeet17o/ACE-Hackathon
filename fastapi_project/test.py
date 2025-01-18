import streamlit as st
import random
import time

# Dummy content generator function
def generate_content(company_details, keywords, content_type="combined"):
    # Simulating AI response
    ads = [
        "Catchy ad for the product with an engaging offer!",
        "Limited-time deal: Save big on your next purchase.",
        "Exclusive discount on our products just for you!",
        "Get started with our product now and enjoy 20% off."
    ]
    
    emails = {
        "subject": "Exciting Opportunity for You!",
        "body": f"Hello {company_details['company_name']},\n\nWe are excited to share an amazing opportunity tailored just for your target audience of {company_details['target_audience']} in {company_details['demographic']['location']}."
    }
    
    blogs = [
        {"idea": "How to Succeed in Marketing", "content": "A detailed blog post about marketing strategies."},
        {"idea": "Boost Your Sales with AI", "content": "This blog explains how AI can transform your sales process."},
        {"idea": "Content Creation Tips", "content": "Best practices for content creation in 2025."},
        {"idea": "Social Media Strategies", "content": "Leveraging social media to grow your business."},
        {"idea": "Understanding Customer Behavior", "content": "A comprehensive guide on analyzing customer data."}
    ]
    
    # Returning the generated content based on type
    if content_type == "combined":
        return {"advertisement": ads, "email": emails, "blog": blogs}
    elif content_type == "email":
        return emails
    elif content_type == "blog":
        return blogs

# Streamlit UI
def app():
    st.title("AI Engagement Platform")
    
    # Sidebar for navigation
    st.sidebar.header("Navigation")
    option = st.sidebar.selectbox("Choose Content Type", ["Content Generator", "Influencer Marketing"])
    
    if option == "Content Generator":
        # Collecting company details
        st.header("Company Details")
        company_name = st.text_input("Company Name", "Dummy Company")
        target_audience = st.text_input("Target Audience", "Young Adults")
        demographic_age = st.text_input("Age Group", "18-35")
        demographic_location = st.text_input("Location", "USA")
        demographic_interests = st.text_input("Interests", "Technology, Fashion, Sports")
        
        # Dummy challenges
        challenges = st.text_area("Challenges", "Increasing brand awareness, Engaging customers")
        
        company_details = {
            "company_name": company_name,
            "target_audience": target_audience,
            "demographic": {
                "age_group": demographic_age,
                "location": demographic_location,
                "interests": demographic_interests
            },
            "challenges": challenges.split("\n")
        }
        
        keywords = st.text_input("Keywords", "AI, Marketing, Technology")
        
        if st.button("Generate Content"):
            with st.spinner("Generating content..."):
                time.sleep(2)  # Simulate API call delay
                
                # Generate content based on the inputs
                generated_content = generate_content(company_details, keywords)
                
                # Display the generated content
                st.subheader("Generated Advertisements")
                for ad in generated_content['advertisement']:
                    st.write(f"- {ad}")
                
                st.subheader("Generated Email")
                email = generated_content['email']
                st.write(f"**Subject:** {email['subject']}")
                st.write(f"**Body:**\n{email['body']}")
                
                st.subheader("Generated Blogs")
                for blog in generated_content['blog']:
                    st.write(f"**Blog Idea:** {blog['idea']}")
                    st.write(f"**Content:**\n{blog['content']}")
                
                # Option to select content type for further exploration
                content_type = st.selectbox("Select Content Type for More", ["Advertisement", "Email", "Blog"])
                
                if content_type == "Advertisement":
                    st.write("Displaying advertisements...")
                    for ad in generated_content['advertisement']:
                        st.write(f"- {ad}")
                
                elif content_type == "Email":
                    st.write("Displaying email content...")
                    st.write(f"**Subject:** {email['subject']}")
                    st.write(f"**Body:**\n{email['body']}")
                
                elif content_type == "Blog":
                    st.write("Displaying blog posts...")
                    for blog in generated_content['blog']:
                        st.write(f"**Blog Idea:** {blog['idea']}")
                        st.write(f"**Content:**\n{blog['content']}")

    elif option == "Influencer Marketing":
        st.write("Influencer Marketing features coming soon!")
        

if __name__ == "__main__":
    app()
