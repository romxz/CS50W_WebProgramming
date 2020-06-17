import os
import requests
from .dbModels import ReviewStats, GoodReadsStats

def review_counts(isbn: str) -> GoodReadsStats:
    gid = getGRid()
    review_data = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": gid, "isbns": isbn}).json()
    review_data = review_data['books'][0]
    counts = dict()
    for data in ['average_rating', 'work_ratings_count']:
        if data not in review_data: continue
        counts[data] = review_data[data]
    return GoodReadsStats(**counts)

def getGRid():
    return os.getenv("GOODREADS_ID")

"""
review_data = goodReads.review_counts(isbn)['books'][0]
            #raise Exception(review_data)
            for data in ['average_rating', 'work_ratings_count']:
                if data not in review_data: continue
                counts[data] = review_data[data]
                """