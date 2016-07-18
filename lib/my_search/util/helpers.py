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

    query_magnitude = [pow(float(value), 2) for value in query.values()]
    article_magnitude = [pow(float(value), 2) for value in article.values()]

    query_magnitude = float(sum(query_magnitude))
    article_magnitude = float(sum(article_magnitude))

    for token in query:
        dot_product += query[token] * article[token]

    return dot_product / query_magnitude * article_magnitude
