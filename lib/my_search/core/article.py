"""
Contains the article class.
"""
from collections import defaultdict


class Article(object):
    """
    Create an artice instance that keeps track of necessary indexed info.
    """

    def __init__(self, article_id, title, frequencies):
        """
        Initialize the article instance.

        Args:
            article_id (str)
            title (str)
            frequencies (dict{str:int})
        """
        self.article_id = article_id
        self.title = title
        self.frequencies = frequencies
        self.tfidf = defaultdict(float)

    def clear_freq(self):
        """
        Clear frequencies before writing to file, to save memory.
        """
        self.frequencies = None

    def add_tfidf(self, token, value):
        """
        Add tfidf value for a given token.

        Args:
            token (str)
            value (float)
        """
        self.tfidf[token] = value
