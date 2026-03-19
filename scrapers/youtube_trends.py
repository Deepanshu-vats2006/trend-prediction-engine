from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
import os
from database.db import insert_youtube

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

    insert_youtube(keyword, video_id, title, channel, published)