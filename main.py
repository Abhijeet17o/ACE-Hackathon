import streamlit as st
import pandas as pd
import plotly.express as px
from huggingface_hub import InferenceClient
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Retrieve the API key from the environment
gemini_api_key = os.getenv("GEMINI_API_KEY")
image_api_key = os.getenv("IMAGE_API_KEY")

# Function for Image Generation
def generate_image(prompt):
    # Instantiate the InferenceClient with your model and token
    client = InferenceClient("black-forest-labs/FLUX.1-dev", token=image_api_key)

    # Generate an image based on the prompt
    image = client.text_to_image(prompt)
    return image

# Function for Text Generation
def generate_text(prompt):
    # Configure Google generative AI API
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Generate content using the model
    response = model.generate_content(prompt)
    return response.text

# Load shopping trends data
shopping_data = pd.read_csv('shopping_trends.csv')

# Extract unique product names for the dropdown menu
unique_products = shopping_data["Item Purchased"].dropna().unique()

# Function to generate processed data for visualizations
def process_shopping_data(data, item_purchased):
    # Filter data for the selected item
    filtered_data = data[data['Item Purchased'] == item_purchased]
    
    # Group by the selected item and generate insights
    age_group_distribution = filtered_data['Age'].value_counts(normalize=True) * 100
    gender_distribution = filtered_data['Gender'].value_counts(normalize=True) * 100
    location_sales = filtered_data.groupby('Location')['Purchase Amount (USD)'].sum().sort_values(ascending=False)
    seasonal_trends = filtered_data.groupby('Season')['Purchase Amount (USD)'].mean()
    avg_purchase_amount = filtered_data['Purchase Amount (USD)'].mean()

    return age_group_distribution, gender_distribution, location_sales, seasonal_trends, avg_purchase_amount

# Main app
st.set_page_config(page_title="Product Insights Hub 📈", layout="wide")
st.title("Product Insights Hub 📈")

# Tabs for Generate Dashboard, Generate Text, and Generate Image
tab1, tab4, tab3, tab2 = st.tabs(["Generate Dashboard", "Sentiment Analysis", "Generate Ad Campaign Image", "Generate Ad Campaign Text"])

# Tab 1: Generate Dashboard
with tab1:
    st.subheader("Generate Dashboard")
    
    item_purchased = st.selectbox("Select the Item Purchased to filter the data:", options=unique_products)

    if st.button("Generate Dashboard"):
        if not item_purchased:
            st.error("Please select an item to generate the dashboard.")
        else:
            st.success(f"Dashboard generated for: {item_purchased}")

            # Process shopping data for the specified item
            age_group_distribution, gender_distribution, location_sales, seasonal_trends, avg_purchase_amount = process_shopping_data(shopping_data, item_purchased)

            # Target Audience Summary
            st.subheader("Target Audience Summary")
            st.markdown(f"""
                **1. Top Age Group:**
                The product '{item_purchased}' is most popular among the age group **{age_group_distribution.idxmax()}**
                ({age_group_distribution.max():.2f}% of consumers).
                
                **2. Top Gender:**
                The product is mostly purchased by **{gender_distribution.idxmax()}** users, accounting for 
                **{gender_distribution.max():.2f}%** of total consumers.
                
                **3. Top Location:**
                The highest sales are recorded in **{location_sales.head(1).index[0]}**, 
                with a total of **${location_sales.head(1).values[0]:.2f}** in sales.
                
                **4. Top Season for Sales:**
                The season with the highest average purchase amount is **{seasonal_trends.idxmax()}**
                with an average purchase amount of **${seasonal_trends.max():.2f}**.
                
                **5. Average Purchase Amount:**
                The average amount spent on this product is **${avg_purchase_amount:.2f}**.
            """)

            # Dashboard Layout
            st.subheader(f"Shopping Trends Overview for {item_purchased}")
            col1, col2 = st.columns(2)

            # Pie chart for Age Group Distribution
            with col1:
                fig_age = px.pie(values=age_group_distribution.values, 
                                 names=age_group_distribution.index, 
                                 title="Age Group Distribution")
                st.plotly_chart(fig_age, use_container_width=True)

            # Pie chart for Gender Distribution
            with col2:
                fig_gender = px.pie(values=gender_distribution.values, 
                                    names=gender_distribution.index, 
                                    title="Gender Distribution")
                st.plotly_chart(fig_gender, use_container_width=True)

            # Location-based Sales (Descending Order)
            st.subheader("Location-Based Sales")
            fig_location = px.bar(location_sales.head(5),  # Only showing top 5 locations
                                  x=location_sales.head(5).index, 
                                  y=location_sales.head(5).values, 
                                  title="Top 5 Sales by Location", 
                                  labels={"x": "Location", "y": "Total Sales"})
            st.plotly_chart(fig_location, use_container_width=True)

            # Seasonal Trends
            st.subheader("Seasonal Trends")
            fig_seasonal = px.line(seasonal_trends, 
                                   x=seasonal_trends.index, 
                                   y=seasonal_trends.values, 
                                   title="Average Purchase Amount by Season", 
                                   labels={"x": "Time of Year", "y": "Average Purchase Amount"})
            st.plotly_chart(fig_seasonal, use_container_width=True)

            # Average Purchase Amount
            st.metric(label="Average Purchase Amount", value=f"${avg_purchase_amount:.2f}")

# Tab 2: Generate Text
with tab2:
    st.subheader("Generate your Ad Campaign Text!")
    
    # Input box for custom prompt (default text is empty)
    text_prompt = st.text_area("Enter the prompt to generate text:", "")
    
    if st.button("Generate Text"):
        if text_prompt:
            response_text = generate_text(text_prompt)
            st.write(response_text)
        else:
            st.error("Please enter a prompt to generate text.")

# Tab 3: Generate Image
with tab3:
    st.subheader("Generate your Ad Campaign Image!")
    
    # Input box for custom prompt (default text is empty)
    image_prompt = st.text_area("Enter the prompt to generate image:", "")
    
    if st.button("Generate Image"):
        if image_prompt:
            image = generate_image(image_prompt)
            st.image(image, caption="Generated Image", use_column_width=True)
        else:
            st.error("Please enter a prompt to generate an image.")

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

# Download the VADER lexicon
nltk.download('vader_lexicon')

# Step 4: Sentiment Analysis
# Initialize the Sentiment Intensity Analyzer
sia = SentimentIntensityAnalyzer()

# Function to analyze sentiment
def analyze_sentiment(comment):
    score = sia.polarity_scores(comment)
    return score

# Function to classify sentiment
def classify_sentiment(score):
    if score['compound'] >= 0.05:
        return 'Positive'
    elif score['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Tab 4: Sentiment Analysis
with tab4:
    st.subheader("Sentiment Analysis of Comments for Selected Product")
    
    # Dropdown to select a specific product
    selected_product = st.selectbox("Select a product to analyze comments:", options=unique_products)
    
    if st.button("Analyze Sentiment for Selected Product"):
        # Filter the data for the selected product
        filtered_data = shopping_data[shopping_data['Item Purchased'] == selected_product]
        
        if filtered_data.empty:
            st.warning(f"No data available for the selected product: {selected_product}")
        elif 'Comments' not in filtered_data.columns:
            st.error("The dataset does not contain a 'Comments' column.")
        else:
            # Perform sentiment analysis on the 'Comments' column
            filtered_data['Sentiment Score'] = filtered_data['Comments'].fillna('').apply(analyze_sentiment)
            filtered_data['Sentiment'] = filtered_data['Sentiment Score'].apply(classify_sentiment)
            
            # Create columns for layout
            col1, col2 = st.columns(2)

            # Column 1: Display the results as a table
            with col1:
                st.subheader(f"Sentiment Analysis Table for '{selected_product}'")
                st.dataframe(filtered_data[['Comments', 'Sentiment']])

            # Column 2: Display the sentiment distribution as a pie chart
            with col2:
                st.subheader(f"Sentiment Distribution for '{selected_product}'")
                sentiment_counts = filtered_data['Sentiment'].value_counts()
                fig_pie = px.pie(
                    values=sentiment_counts.values,
                    names=sentiment_counts.index,
                    title="Sentiment Distribution",
                    color=sentiment_counts.index,
                    color_discrete_map={"Positive": "green", "Negative": "red", "Neutral": "gray"}
                )
                st.plotly_chart(fig_pie, use_container_width=True)
