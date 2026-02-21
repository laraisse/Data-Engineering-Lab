from capture_python import ingest_reviews_from_csv
from transform import transform_reviews

print('ingesting csv')
ingest_reviews_from_csv(
    "../data/raw/note_taking_ai_reviews_batch2.csv"
)
print('transforming reviews')
transform_reviews(
    input_file="apps_reviews_batch2.json"
)
