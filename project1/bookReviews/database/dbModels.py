from typing import NamedTuple, TypedDict

class Book(TypedDict):
    """Represents a book."""
    isbn: str
    title: str
    author: str
    year: int

class User(TypedDict):
    """Represents a user."""
    id: int
    username: str
    khash: str

class DatabaseReview(TypedDict):
    """Represents a review in the database."""
    uid: int
    isbn: str
    rating: float
    review: str

class UserReview(TypedDict):
    """Username version of Review for display."""
    username: str
    rating: float
    review: str

class ReviewStats(TypedDict):
    """Represents internal review stats for a book."""
    review_count: int
    average_score: 'None' = None

class GoodReadsStats(TypedDict, total=False):
    """Represents GoodReads book review stats from GoodReads"""
    work_ratings_count: int
    average_rating: float