# src/main.py

from capture import extract_apps, extract_reviews_paginated
from transform import transform_apps, transform_reviews
from serve import create_app_level_kpis, create_daily_metrics
from dashboard import run_dashboard
import os

def main():
    print('extracting apps')
    apps = extract_apps()
    print("Extracting reviews")
    extract_reviews_paginated(apps)

    print('transforming apps')
    transform_apps()
    print('transforming reviews')
    transform_reviews()

    print('Creating app-level KPIs')
    create_app_level_kpis()
    print('Creating daily metrics')
    create_daily_metrics()

    run_dashboard()


if __name__ == "__main__":
    main()
