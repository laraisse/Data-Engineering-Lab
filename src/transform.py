# src/transform.py

import json
import os
import pandas as pd

RAW_PATH = "../data/raw"
PROCESSED_PATH = "../data/processed"

os.makedirs(PROCESSED_PATH, exist_ok=True)

def transform_apps():
    with open(f"{RAW_PATH}/apps_metadata.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.json_normalize(data)

    expected_columns = [
        "appId",
        "title",
        "developer",
        "score",
        "ratings",
        "installs",
        "genre",
        "price"
    ]

    for col in expected_columns:
        if col not in df.columns:
            df[col] = None

    apps = df[expected_columns]

    apps.to_csv(
        f"{PROCESSED_PATH}/apps_catalog.csv",
        index=False
    )



def transform_reviews(
    input_file="apps_reviews.json",
    output_file="apps_reviews_clean.csv"
):
    with open(f"{RAW_PATH}/{input_file}", "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.json_normalize(data)

    expected_columns = [
        "appId",
        "appName",
        "reviewId",
        "userName",
        "score",
        "content",
        "thumbsUpCount",
        "at"
    ]

    for col in expected_columns:
        if col not in df.columns:
            df[col] = None

    reviews = df[expected_columns]

    reviews["at"] = pd.to_datetime(
        reviews["at"], errors="coerce"
    )

    reviews["score"] = pd.to_numeric(
        reviews["score"], errors="coerce"
    )

    reviews["thumbsUpCount"] = pd.to_numeric(
        reviews["thumbsUpCount"], errors="coerce"
    ).fillna(0)

    reviews.to_csv(
        f"{PROCESSED_PATH}/{output_file}",
        index=False
    )
