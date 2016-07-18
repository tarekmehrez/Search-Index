"""
Contains the SearchDriver class.
"""

from index import Index
from my_search.util import io
from my_search.util import preprocessing


class SearchEngine(object):

    """
    Create a search engine.

    - Build an index on the given knowledge base
    - Tokenize query
    - Get intersection of postings
    - Return search results accoridngly
    """

    def __init__(self):
        """
        Initialize a search engine instance.
        """
        self._index = None

    def build_index(self, path_to_knwoledge_base, path_to_index):
        """
        Take in file with articles, create an index instance.

        Args:
            path_to_knwoledge_base(str)
            path_to_index(str)
        """
        # in case index is found, load it
        if io.exists(path_to_index):
            self._index = io.read(path_to_index)
            return

        # otherwise, create it
        raw_content = io.read(path_to_knwoledge_base)
        self._index = Index()
        self._index.build_index(raw_content)

        io.write(self._index)

    def search(self, query):
        """
        Run the search engine for a given query.

        Args:
            query (str)
        Returns
            list[list[str]]: results as article ids and titles
        """
        tokens = preprocessing.tokenize(query)
        results = self._postings_intersections(tokens)

        # TODO ranking

        return results

    def _postings_intersections(self, tokens):
        """
        Return intersection of postings for given tokens.

        Args:
            tokens (list[str])
        Returns:
            dict{id, title}: article ids and their titles
        """
        # get article intersection for all tokens
        intersection = set()
        for token in tokens:
            articles = self._index.postings[token].keys()
            intersection &= set(articles)

        # get their titles
        result = {}
        for article_id in intersection:
            result[article_id] = self._index.articles[article_id]

        return result
