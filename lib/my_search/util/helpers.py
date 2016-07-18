"""
Contains some helper functions.
"""
from math import pow


def cosine_similarity(query, article)
    """
    Given two tfidf dicts, calculate the cosine distance between them.

    Args:
        query (dict{str: float})
        article (dict{str: float})
    Returns:
        float: cosine similarity
    """
    dot_product = 0.0

    query_magnitude = _calculate_magnitude(query.values())
    article_magnitude = _calculate_magnitude(article.values())

    # assuming query is always smaller than article
    for token in query:
        dot_product += query[token] * article[token]

    return dot_product / query_magnitude * article_magnitude


def _calculate_magnitude(vector):
    """
    Calculate a magnitude of a vector.

    Args:
        vector (list[int])
    Retirns:
        float: magnitude
    """
    magnitude = [pow(float(value), 2) for value in vector]
    return float(sum(magnitude))
