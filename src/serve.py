# src/serve.py

import pandas as pd
import os

PROCESSED_PATH = "../data/processed"


def create_app_level_kpis():
    df = pd.read_csv(f"{PROCESSED_PATH}/apps_reviews_clean.csv")
    df["at"] = pd.to_datetime(df["at"])

    kpis = (
        df.groupby(["appId", "appName"])
        .agg(
            number_of_reviews=("reviewId", "count"),
            average_rating=("score", "mean"),
            low_rating_pct=("score", lambda x: (x <= 2).mean() * 100),
            first_review=("at", "min"),
            last_review=("at", "max")
        )
        .reset_index()
    )

    kpis.to_csv(f"{PROCESSED_PATH}/app_level_kpis.csv", index=False)


def create_daily_metrics():
    df = pd.read_csv(f"{PROCESSED_PATH}/apps_reviews_clean.csv")
    df["at"] = pd.to_datetime(df["at"])
    df["date"] = df["at"].dt.date

    daily = (
        df.groupby("date")
        .agg(
            daily_reviews=("reviewId", "count"),
            daily_avg_rating=("score", "mean")
        )
        .reset_index()
    )

    daily.to_csv(f"{PROCESSED_PATH}/daily_metrics.csv", index=False)
