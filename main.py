from database.db import create_tables
from scrapers.google_trends import run_google_trends
from scrapers.youtube_trends import run_youtube_trends

def main():
    print("🚀 Trend Engine Started...\n")

    create_tables()

    keywords = input("Enter keywords (comma separated): ").split(",")

    keywords = [k.strip() for k in keywords]

    run_google_trends(keywords)
    run_youtube_trends(keywords)

    print("\n✅ Data stored successfully!")

if __name__ == "__main__":
    main()