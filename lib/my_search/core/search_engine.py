"""
Contains the SearchDriver class.
"""
import operator
from collections import OrderedDict

from index import Index
from my_search.util import io
from my_search.util import preprocessing
from my_search.util import helpers


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
        frequencies = preprocessing.count_frequency(tokens)

        articles = self._postings_intersections(frequencies.keys())
        ranked_scores = self._rank(frequencies, articles)

        article_ids = ranked_scores.keys()
        titles = [self.index.articles[article_id]
                  for article_id in article_ids]

        return zip(article_ids, titles)

    def _postings_intersections(self, tokens):
        """
        Return intersection of postings for given tokens.

        Args:
            tokens (list[str])
        Returns:
            dict{str, str}: article ids and their titles
        """
        # get article intersection for all tokens
        intersection = set()
        for token in tokens:
            articles = self._index.postings[token]
            intersection &= articles

        # get their titles
        result = {}
        for article_id in intersection:
            result[article_id] = self._index.articles[article_id]

        return result

    def _rank(self, frequencies, articles):
        """
        Rank returned search results.

        Args:
            frequencies (dict{str:int})
            articles (dict{str, str}): article ids and their titles

        Returns:
            OrderedDict
        """
        # lookup tfidf values of returned articles
        returned_articles_tfidf = {}
        for article_id in articles:
            returned_articles_tfidf[
                article_id] = self.index.article_tfidf[article_id]

        # calculate tfidf of current query
        query_tfidf = {}
        for token, frequency in frequencies.iteritems():
            query_tfidf[token] = float(
                frequency) * float(self.index.token_idf[token])

        # calculate cosine similarities
        similarity_scores = {}

        for article_id in returned_articles_tfidf:
            current_score = helpers.cosine_similarity(
                query_tfidf, returned_articles_tfidf[article_id])

            similarity_scores[article_id] = current_score

        # sort according to scores ~ rank search results
        sorted_scores = sorted(similarity_scores.items(),
                               key=operator.itemgetter(1))

        return OrderedDict(sorted_scores)
