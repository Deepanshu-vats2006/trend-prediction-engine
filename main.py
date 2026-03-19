from database.db import create_tables
from scrapers.google_trends import run_google_trends
from scrapers.youtube_trends import run_youtube_trends
from analysis.trend_score import show_top_trends
from analysis.visualize import plot_bar_chart, plot_pie_chart
import time

def get_keywords():
    user_input = input("Enter keywords (comma-separated, max 5): ")
    keywords = [word.strip() for word in user_input.split(",")]

    if len(keywords) > 5:
        print("Maximum 5 keywords allowed")
        exit()

    return keywords


def main():
    print("🚀 Trend Engine Started...\n")

    # Step 1: Setup DB
    create_tables()

    # Step 2: Get input
    keywords = get_keywords()

    # Step 3: Run scrapers
    run_google_trends(keywords)
    run_youtube_trends(keywords)

    print("\n✅ Data stored successfully in database!")

    # Step 4: Analyze trends
    time.sleep(1)  # Simulate processing time
    show_top_trends()

    # Step 5: Visualize data 
    plot_bar_chart()
    plot_pie_chart()

if __name__ == "__main__":
    main()