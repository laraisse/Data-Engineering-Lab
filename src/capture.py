# src/capture.py

import json
import os
import pandas as pd
from google_play_scraper import search, app, reviews, Sort

RAW_PATH = "../data/raw"
KEYWORD = "AI note taking"

os.makedirs(RAW_PATH, exist_ok=True)



def extract_apps(n_apps=20):
    results = search(
        KEYWORD,
        lang="en",
        country="us",
        n_hits=n_apps
    )

    apps = []
    for r in results:
        apps.append(app(r["appId"], lang="en", country="us"))

    with open(f"{RAW_PATH}/apps_metadata.json", "w", encoding="utf-8") as f:
        json.dump(apps, f, ensure_ascii=False, indent=2)

    return apps


def extract_reviews_paginated(
    apps,
    max_pages=3,
    page_size=100,
    output_file="apps_reviews.json"
):
    all_reviews = []

    for a in apps:
        app_id = a["appId"]
        app_name = a["title"]

        continuation_token = None

        for _ in range(max_pages):
            revs, continuation_token = reviews(
                app_id,
                lang="en",
                country="us",
                sort=Sort.NEWEST,
                count=page_size,
                continuation_token=continuation_token
            )

            for r in revs:
                r["appId"] = app_id
                r["appName"] = app_name
                all_reviews.append(r)

            if continuation_token is None:
                break

    with open(f"{RAW_PATH}/{output_file}", "w", encoding="utf-8") as f:
        json.dump(
            all_reviews,
            f,
            ensure_ascii=False,
            indent=2,
            default=str
        )



def ingest_reviews_from_csv(
    csv_path,
    output_file="apps_reviews_batch2.json"
):
    df = pd.read_csv(csv_path)

    # store as raw JSON to keep pipeline consistent
    json_path = f"{RAW_PATH}/{output_file}"
    df.to_json(
        json_path,
        orient="records",
        force_ascii=False
    )

    return output_file
