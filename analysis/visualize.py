import matplotlib.pyplot as plt
from analysis.trend_score import calculate_final_score


def plot_bar_chart():
    trends = calculate_final_score()

    if not trends:
        print("❌ No data to visualize")
        return

    keywords = [item[0] for item in trends[:5]]
    scores = [item[1] for item in trends[:5]]

    plt.figure()
    plt.bar(keywords, scores)
    plt.title("Top Trending Keywords")
    plt.xlabel("Keywords")
    plt.ylabel("Score")

    plt.show()


def plot_pie_chart():
    trends = calculate_final_score()

    if not trends:
        print("❌ No data to visualize")
        return

    keywords = [item[0] for item in trends[:5]]
    scores = [item[1] for item in trends[:5]]

    plt.figure()
    plt.pie(scores, labels=keywords, autopct='%1.1f%%')
    plt.title("Trend Distribution")

    plt.show()