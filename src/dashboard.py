# src/dashboard.py

import pandas as pd
import matplotlib.pyplot as plt

PROCESSED_PATH = "../data/processed"


def run_dashboard():
    apps = pd.read_csv(f"{PROCESSED_PATH}/app_level_kpis.csv")
    daily = pd.read_csv(f"{PROCESSED_PATH}/daily_metrics.csv")

    # 1️⃣ Best vs worst apps
    apps_sorted = apps.sort_values("average_rating")

    plt.figure()
    plt.barh(apps_sorted["appName"], apps_sorted["average_rating"])
    plt.title("Average Rating per App")
    plt.xlabel("Rating")
    plt.show()

    # 2️⃣ Review volume vs rating
    plt.figure()
    plt.scatter(
        apps["number_of_reviews"],
        apps["average_rating"]
    )
    plt.xlabel("Number of Reviews")
    plt.ylabel("Average Rating")
    plt.title("Popularity vs Satisfaction")
    plt.show()

    # 3️⃣ Rating trend over time
    plt.figure()
    plt.plot(
        pd.to_datetime(daily["date"]),
        daily["daily_avg_rating"]
    )
    plt.title("Average Rating Over Time")
    plt.xlabel("Date")
    plt.ylabel("Rating")
    plt.show()
