from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
import os
from database.db import insert_trend
from datetime import datetime

load_dotenv()  

def run_youtube_trends(keywords):
    api_key = os.getenv("YOUTUBE_API_KEY")

    youtube = build("youtube", "v3", developerKey=api_key)

    for keyword in keywords:
        print(f"\n🔎 YouTube results for: {keyword}")

        request = youtube.search().list(
            part="snippet",
            q=keyword,
            maxResults=5
        )

        response = request.execute()

        for item in response["items"]:

            if "videoId" not in item["id"]:
                   continue   # skip non-video results

            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            channel = item["snippet"]["channelTitle"]
            published = item["snippet"]["publishedAt"]

    print("-", title)

    insert_trend(
    title=keyword,
    platform="youtube",
    score=1,  # each video = 1 weight
    timestamp=published
)