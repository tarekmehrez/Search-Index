"""
Contains package-specific exceptions.
"""


class FormatNotSupportedException(Exception):

    """
    Format not supported exception while doing io operations.
    """
    pass


class QueryTooLongException(Exception):

    """
    In case Query is longer than the article, while doing tfidf sim measure.
    """
    pass


class IndexNotLoadedException(Exception):
    """
    If user is searching before creating/loading an index.
    """
    pass