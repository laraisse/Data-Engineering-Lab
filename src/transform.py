# src/transform.py

import json
import pandas as pd
import os

RAW_PATH = "../data/raw"
PROCESSED_PATH = "../data/processed"

os.makedirs(PROCESSED_PATH, exist_ok=True)


def transform_apps():
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
            "price"
        ]
    ]

    apps.to_csv(f"{PROCESSED_PATH}/apps_catalog.csv", index=False)


def transform_reviews():
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
            "at"
        ]
    ]

    reviews["at"] = pd.to_datetime(reviews["at"], errors="coerce")

    reviews.to_csv(
        f"{PROCESSED_PATH}/apps_reviews_clean.csv",
        index=False
    )
