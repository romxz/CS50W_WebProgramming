import os
import requests
import json

def review_counts(isbn: str):
    gid = getGRid()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": gid, "isbns": isbn})
    return res.json()
    #return json.load(res.json())

def getGRid():
    return os.getenv("GOODREADS_ID")