"""
Contains some helper functions.
"""
from math import pow
from math import sqrt
from math import acos

from my_search.exceptions import QueryTooLongException

DECIMAL_PLACES = 3


def cosine_similarity(query, article):
    """
    Given two tfidf dicts, calculate the cosine distance between them.

    Args:
        query (dict{str: float})
        article (dict{str: float})
    Returns:
        float: cosine similarity
    """
    if len(query) > len(article):
        raise QueryTooLongException(
            'query has length %s, while article has length %s' %
            (len(query), len(article)))

    dot_product = 0.0

    query_magnitude = _calculate_magnitude(query.values())
    article_magnitude = _calculate_magnitude(article.values())

    # assuming query is always smaller than article
    for token in query:
        dot_product += query[token] * article[token]

    final_product = dot_product / (query_magnitude * article_magnitude)
    rounded_value = round(final_product, DECIMAL_PLACES)

    return acos(rounded_value)


def _calculate_magnitude(vector):
    """
    Calculate a magnitude of a vector.

    Args:
        vector (list[int])
    Retirns:
        float: magnitude
    """
    magnitude = [pow(float(value), 2) for value in vector]
    return sqrt(float(sum(magnitude)))
