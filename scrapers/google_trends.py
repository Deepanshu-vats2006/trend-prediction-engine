import time
from pytrends.request import TrendReq
from database.db import insert_trend
from datetime import datetime

def run_google_trends(keywords):
    print("🔥 Running Google Trends...")

    pytrends = TrendReq(hl="en-US", tz=330)
    time.sleep(5)

    data = None

    for attempt in range(3):
        try:
            print(f"Attempt {attempt + 1}...")

            pytrends.build_payload(
                keywords,
                timeframe="now 7-d",
                geo=''
            )
            data = pytrends.interest_over_time()

            print("✅ Data received")
            break

        except Exception as e:
            print("❌ Error:", str(e))
            time.sleep(10)

    if data is None or data.empty:
        print("⚠️ No Google Trends data")
        return

    # 🔥 REMOVE EXTRA COLUMN
    if "isPartial" in data:
        data = data.drop(columns=["isPartial"])

    # ✅ YOUR ADDED CODE (CORRECT PLACE)
    print("\n📊 Google Trends Data:\n")
    print(data.head(10))   # show first 10 rows

    # 💾 STORE DATA
    for keyword in keywords:
        if keyword in data:
            for index, row in data.iterrows():
                insert_trend(
                title=keyword,
                platform="google",
                score=int(row[keyword]),
                timestamp=str(index)
            )
    print("✅ Google Trends stored (no duplicates)")