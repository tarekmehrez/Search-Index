"""
Contains the SearchDriver class.
"""
import operator
from collections import OrderedDict

from index import Index

from my_search.util import io
from my_search.util import logger
from my_search.util import preprocessing
from my_search.util import helpers
from my_search.exceptions import IndexNotLoadedException


# done logging statements are there to track time taken to perform operations
_logger = logger.init_logger()


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
        self.index = Index()

    def build_index(self, path_to_knwoledge_base, path_to_index_dir):
        """
        Take in file with articles, create an index instance.

        Args:
            path_to_knwoledge_base(str)
            path_to_index(str)
        """
        # in case index is found, load it
        if io.exists(path_to_index_dir):
            _logger.info('Index located at %s already exists', path_to_index_dir)
            self.load_index(path_to_index_dir)
            return

        _logger.info('Creating index from knowledge base %s', path_to_knwoledge_base)

        # otherwise, create it
        raw_content = io.read(path_to_knwoledge_base)

        _logger.debug('Creating postings')
        self.index.build_index(raw_content)
        _logger.debug('Calculating tfidf')
        self.index.calculate_tfidf()
        _logger.debug('Writing index')
        self.index.save(path_to_index_dir)
        _logger.debug('Done writing index')

    def load_index(self, path_to_index_dir):
        """
        Load index instance.
        """
        _logger.debug('Loading index from %s', path_to_index_dir)
        self._index = self.index.load(path_to_index_dir)
        _logger.debug('Done loading index')

    def search(self, query, num_of_results):
        """
        Run the search engine for a given query.

        Args:
            query (str)
            num_of_results (int): number of results to be returned
        Returns
            list[list[str]]: results as article ids and titles
        """
        if self.index is None:
            raise IndexNotLoadedException('You need to create or load index first')

        tokens = preprocessing.tokenize(query)

        frequencies = preprocessing.count_frequency(tokens)
        articles = self._postings_intersections(frequencies.keys())

        if len(articles) == 0:
            return []

        ranked_scores = self._rank(frequencies, articles)

        article_ids = ranked_scores.keys()
        titles = [self.index.articles[article_id].title
                  for article_id in article_ids]

        results = zip(article_ids, titles)

        return results[:num_of_results]

    def _postings_intersections(self, tokens):
        """
        Return intersection of postings for given tokens.

        Args:
            tokens (list[str])
        Returns:
            dict{str, str}: article ids and their titles
        """
        # get article intersection for all tokens
        set_list = [self.index.postings[token] for token in tokens]
        intersection = set.intersection(*set_list)

        # get their titles
        result = {}
        for article_id in intersection:
            result[article_id] = self.index.articles[article_id].title

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
                article_id] = self.index.articles[article_id].tfidf

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
