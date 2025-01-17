import google.generativeai as genai
import re
import pandas as pd
from googleapiclient.discovery import build
import json
import os

# Configure the Google Gemini API
genai.configure(api_key=os.getenv('GENAI_API_KEY'))

generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

def process_input_with_gemini(input_text):
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(input_text)
    return response.text.strip()

def extract_details_from_gemini_response(response):
    categories = []
    age_group = None

    categories_match = re.findall(r"Categories: ([^\n]+)", response)
    age_group_match = re.findall(r"Age Group: ([^\n]+)", response)

    if categories_match:
        categories = [cat.strip() for cat in categories_match[0].split(",")]
    if age_group_match:
        age_group = age_group_match[0].strip()

    if not categories or not age_group:
        raise ValueError("Model's response is invalid or does not match the expected format.")

    return categories, age_group

def fetch_youtube_channels(categories, cpm=5):
    youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))
    account_names = []

    for category in categories:
        try:
            search_response = youtube.search().list(
                q=category,
                part='snippet',
                type='channel',
                maxResults=10,
                order='viewCount'
            ).execute()

            if 'items' not in search_response or not search_response['items']:
                continue

            for item in search_response['items']:
                channel_title = item['snippet']['channelTitle']
                channel_id = item['snippet']['channelId']

                channel_response = youtube.channels().list(
                    part='contentDetails,statistics',
                    id=channel_id
                ).execute()

                if 'items' not in channel_response or not channel_response['items']:
                    continue

                upload_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                shorts_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists'].get('shorts', None)

                video_count = 0
                recent_views = []

                playlist_response = youtube.playlistItems().list(
                    part='snippet',
                    playlistId=upload_playlist_id,
                    maxResults=5
                ).execute()

                if 'items' in playlist_response:
                    video_count += len(playlist_response['items'])
                    for video in playlist_response['items']:
                        video_id = video['snippet']['resourceId']['videoId']
                        video_stats = youtube.videos().list(part='statistics', id=video_id).execute()
                        views = int(video_stats['items'][0]['statistics'].get('viewCount', 0))
                        recent_views.append(views)

                if shorts_playlist_id:
                    playlist_response = youtube.playlistItems().list(
                        part='snippet',
                        playlistId=shorts_playlist_id,
                        maxResults=5
                    ).execute()

                    if 'items' in playlist_response:
                        video_count += len(playlist_response['items'])
                        for video in playlist_response['items']:
                            video_id = video['snippet']['resourceId']['videoId']
                            video_stats = youtube.videos().list(part='statistics', id=video_id).execute()
                            views = int(video_stats['items'][0]['statistics'].get('viewCount', 0))
                            recent_views.append(views)

                if video_count == 0:
                    continue

                avg_recent_views = sum(recent_views) / len(recent_views) if recent_views else 0
                subscribers = int(channel_response['items'][0]['statistics']['subscriberCount'])
                total_views = int(channel_response['items'][0]['statistics'].get('viewCount', 0))
                view_to_subscriber_ratio = total_views / subscribers if subscribers > 0 else 0

                if subscribers < 10000 or subscribers >= 200000:
                    continue

                if view_to_subscriber_ratio < 0.1:
                    continue

                promo_seconds = 60
                estimated_dollars = (avg_recent_views * promo_seconds / 1000) * cpm

                account_names.append({
                    'Account Name': channel_title,
                    'Channel ID': channel_id,
                    'Subscribers': subscribers,
                    'Total Views': total_views,
                    'View to Subscriber Ratio': view_to_subscriber_ratio,
                    'Average Recent Views': avg_recent_views,
                    'ROI (Dollars)': estimated_dollars
                })
        except Exception:
            continue

    account_names_sorted = sorted(account_names, key=lambda x: x['ROI (Dollars)'], reverse=True)
    return account_names_sorted[:5]
