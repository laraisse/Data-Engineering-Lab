import os
import pandas as pd
import plotly.express as px

PROCESSED_PATH = "../data/processed"
IMAGE_PATH = "../images"  # folder to save plots

# Create the folder if it doesn't exist
os.makedirs(IMAGE_PATH, exist_ok=True)

def run_dashboard():
    apps = pd.read_csv(f"{PROCESSED_PATH}/app_level_kpis.csv")
    daily = pd.read_csv(f"{PROCESSED_PATH}/daily_metrics.csv")

    # ----------------------------
    # 1️⃣ App performance overview
    # ----------------------------
    fig1 = px.scatter(
        apps,
        x="number_of_reviews",
        y="average_rating",
        size="number_of_reviews",
        color="low_rating_pct",
        hover_name="appName",
        title="App Performance: Popularity vs Satisfaction",
        labels={
            "number_of_reviews": "Number of Reviews",
            "average_rating": "Average Rating",
            "low_rating_pct": "% Low Ratings (≤ 2)"
        },
        color_continuous_scale="RdYlGn_r"
    )
    fig1.show()
    fig1.write_image(f"{IMAGE_PATH}/app_performance.png")

    # ----------------------------
    # 2️⃣ Rating trend over time
    # ----------------------------
    fig2 = px.line(
        daily,
        x="date",
        y="daily_avg_rating",
        title="Average User Rating Over Time",
        labels={
            "date": "Date",
            "daily_avg_rating": "Average Rating"
        }
    )
    fig2.show()
    fig2.write_image(f"{IMAGE_PATH}/rating_trend.png")

    # --------------------------------
    # 3️⃣ Apps with most unhappy users
    # --------------------------------
    worst_apps = apps.sort_values("low_rating_pct", ascending=False).head(10)

    fig3 = px.bar(
        worst_apps,
        x="low_rating_pct",
        y="appName",
        orientation="h",
        title="Apps with Highest Percentage of Low Ratings",
        labels={
            "low_rating_pct": "% Low Ratings (≤ 2)",
            "appName": "Application"
        },
        color="low_rating_pct",
        color_continuous_scale="Reds"
    )
    fig3.show()
    fig3.write_image(f"{IMAGE_PATH}/worst_apps.png")
