import json
import os
import pandas as pd
from google_play_scraper import search, app, reviews, Sort
import datetime


RAW_PATH = "../data"
KEYWORD = "AI note taking"

os.makedirs(RAW_PATH, exist_ok=True)


def extract_apps(n_apps=20):
    results = search(
        KEYWORD,
        lang="en",
        country="us",
        n_hits=n_apps
    )

    apps_list = []
    for r in results:
        apps_list.append(app(r["appId"], lang="en", country="us"))

    # Save as JSONL
    with open(f"{RAW_PATH}/apps_metadata.jsonl", "w", encoding="utf-8") as f:
        for a in apps_list:
            f.write(json.dumps(a, ensure_ascii=False) + "\n")

    return apps_list

def convert_datetime_to_str(obj):
    """
    Recursively convert datetime objects in a dict to ISO strings
    """
    if isinstance(obj, dict):
        return {k: convert_datetime_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetime_to_str(v) for v in obj]
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat()
    else:
        return obj


def extract_reviews_paginated(
    apps,
    max_pages=3,
    page_size=100,
    output_file="apps_reviews.jsonl"
):
    with open(f"{RAW_PATH}/{output_file}", "w", encoding="utf-8") as f:
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
                    # Add app info
                    r["appId"] = app_id
                    r["appName"] = app_name

                    # Convert all datetime objects in the review to strings
                    r = convert_datetime_to_str(r)

                    # Write to JSONL
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")

                if continuation_token is None:
                    break

def ingest_reviews_from_csv(
    csv_path,
    output_file="apps_reviews_batch2.jsonl"
):
    df = pd.read_csv(csv_path)

    json_path = f"{RAW_PATH}/{output_file}"

    with open(json_path, "w", encoding="utf-8") as f:
        for record in df.to_dict(orient="records"):
            for k, v in record.items():
                if isinstance(v, pd.Timestamp):
                    record[k] = v.isoformat()
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return output_file


print('Extracting apps...')
apps = extract_apps()
print("Extracting reviews...")
extract_reviews_paginated(apps)