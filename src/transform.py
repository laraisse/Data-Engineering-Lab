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
    output_file="apps_reviews_clean.csv",
    enable_data_quality_checks=False
):
    with open(f"{RAW_PATH}/{input_file}", "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.json_normalize(data)

    column_mapping = {
        "appId": "appId",
        "appName": "appName",
        "reviewId": "reviewId",
        "userName": "userName",
        "score": "score",
        "content": "content",
        "thumbsUpCount": "thumbsUpCount",
        "at": "at",

        "app_id": "appId",
        "appTitle": "appName",
        "review_id": "reviewId",
        "username": "userName",
        "rating": "score",
        "review_text": "content",
        "thumbs_up": "thumbsUpCount",
        "timestamp": "at",
        "app_name": "appName"
    }
    rename_dict = {col: column_mapping[col] for col in df.columns if col in column_mapping}
    df.rename(columns=rename_dict, inplace=True)

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

    reviews = df.loc[:, expected_columns].copy()
    if enable_data_quality_checks:
        # Track data quality issues
        initial_count = len(reviews)

        # Clean content field: handle NULL strings, empty strings, whitespace
        reviews["content"] = reviews["content"].replace(["NULL", "null", ""], None)
        reviews["content"] = reviews["content"].apply(
            lambda x: None if isinstance(x, str) and x.strip() == "" else x
        )

        # Clean numeric fields: handle text representations of null
        for col in ["thumbsUpCount", "score"]:
            reviews[col] = reviews[col].replace(
                ["NULL", "null", "N/A", "n/a", ""], None
            )

    reviews["at"] = pd.to_datetime(
        reviews["at"], errors="coerce"
    )

    reviews["score"] = pd.to_numeric(
        reviews["score"], errors="coerce"
    )

    reviews["thumbsUpCount"] = pd.to_numeric(
        reviews["thumbsUpCount"], errors="coerce"
    ).fillna(0)

    if enable_data_quality_checks:
        # Enforce business rules for score (must be 1-5)
        reviews.loc[reviews["score"] < 1, "score"] = 1
        reviews.loc[reviews["score"] > 5, "score"] = 5

        # Enforce business rules for thumbsUpCount (must be >= 0)
        reviews.loc[reviews["thumbsUpCount"] < 0, "thumbsUpCount"] = 0

        # Drop reviews with critical missing data
        reviews = reviews.dropna(subset=["reviewId", "score"])
    reviews.to_csv(
        f"{PROCESSED_PATH}/{output_file}",
        index=False
    )
