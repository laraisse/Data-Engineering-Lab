import json
import os
from google_play_scraper import search, app, reviews_all
import pandas as pd
import matplotlib.pyplot as plt

# Paths & config
RAW_PATH = "../data/raw"
PROCESSED_PATH = "../data/processed"
KEYWORD = "AI note taking"

os.makedirs(RAW_PATH, exist_ok=True)
os.makedirs(PROCESSED_PATH, exist_ok=True)

# 1. Data Acquisition
def extract_apps():
    print("Extracting apps metadata...")
    results = search(
        KEYWORD,
        lang="en",
        country="us",
        n_hits=20
    )

    apps_data = []
    for r in results:
        details = app(r["appId"], lang="en")
        apps_data.append(details)

    with open(f"{RAW_PATH}/apps_metadata.json", "w", encoding="utf-8") as f:
        json.dump(apps_data, f, ensure_ascii=False, indent=2)

    return apps_data


def extract_reviews(apps):
    print("Extracting reviews...")
    all_reviews = []

    for a in apps:
        app_id = a["appId"]
        revs = reviews_all(app_id, lang="en", country="us")
        for r in revs:
            r["appId"] = app_id
            r["appName"] = a["title"]

            if "at" in r and r["at"] is not None:
                r["at"] = r["at"].isoformat()

            all_reviews.append(r)

    with open(f"{RAW_PATH}/apps_reviews.json", "w", encoding="utf-8") as f:
        json.dump(all_reviews, f, ensure_ascii=False, indent=2)


# 2. Transformation
def transform_apps():
    print("Transforming apps metadata...")
    with open(f"{RAW_PATH}/apps_metadata.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.json_normalize(data)

    apps = df[
        [
            "appId",
            "title",
            "developer",
            "score",
            "ratings",
            "installs",
            "genre",
            "price",
        ]
    ]

    apps.to_csv(f"{PROCESSED_PATH}/apps_catalog.csv", index=False)


def transform_reviews():
    print("Transforming reviews...")
    with open(f"{RAW_PATH}/apps_reviews.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.json_normalize(data)

    reviews = df[
        [
            "appId",
            "appName",
            "reviewId",
            "userName",
            "score",
            "content",
            "thumbsUpCount",
            "at",
        ]
    ]

    reviews["at"] = pd.to_datetime(reviews["at"], errors="coerce")

    reviews.to_csv(
        f"{PROCESSED_PATH}/apps_reviews_clean.csv", index=False
    )


# 3. Serving Layer
def create_app_level_kpis():
    print("Creating app-level KPIs...")
    df = pd.read_csv(f"{PROCESSED_PATH}/apps_reviews_clean.csv")
    df["at"] = pd.to_datetime(df["at"])

    kpis = (
        df.groupby(["appId", "appName"])
        .agg(
            number_of_reviews=("reviewId", "count"),
            average_rating=("score", "mean"),
            low_rating_percentage=(
                "score",
                lambda x: (x <= 2).mean() * 100,
            ),
            first_review_date=("at", "min"),
            most_recent_review_date=("at", "max"),
        )
        .reset_index()
    )

    kpis.to_csv(
        f"{PROCESSED_PATH}/app_level_kpis.csv", index=False
    )


def create_daily_metrics():
    print("Creating daily metrics...")
    df = pd.read_csv(f"{PROCESSED_PATH}/apps_reviews_clean.csv")
    df["at"] = pd.to_datetime(df["at"])
    df["date"] = df["at"].dt.date

    daily = (
        df.groupby("date")
        .agg(
            daily_number_of_reviews=("reviewId", "count"),
            daily_average_rating=("score", "mean"),
        )
        .reset_index()
    )

    daily.to_csv(
        f"{PROCESSED_PATH}/daily_metrics.csv", index=False
    )

# 4. Dashboard
def run_dashboard():
    print("Launching dashboard...")
    apps = pd.read_csv(f"{PROCESSED_PATH}/app_level_kpis.csv")
    daily = pd.read_csv(f"{PROCESSED_PATH}/daily_metrics.csv")

    # App performance
    apps_sorted = apps.sort_values("average_rating", ascending=False)

    plt.figure()
    plt.barh(apps_sorted["appName"], apps_sorted["average_rating"])
    plt.title("Average Rating per App")
    plt.xlabel("Rating")
    plt.ylabel("App")
    plt.show()

    # Ratings over time
    plt.figure()
    plt.plot(
        pd.to_datetime(daily["date"]),
        daily["daily_average_rating"],
    )
    plt.title("Average Rating Over Time")
    plt.xlabel("Date")
    plt.ylabel("Rating")
    plt.show()

# Main pipeline
def main():
    apps = extract_apps()
    extract_reviews(apps)

    transform_apps()
    transform_reviews()

    create_app_level_kpis()
    create_daily_metrics()

    run_dashboard()


if __name__ == "__main__":
    main()

