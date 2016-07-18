"""
Contains the Index class.
"""
import os
from math import log
from collections import defaultdict

from article import Article

from my_search.util import preprocessing
from my_search.util import io
from my_search.util import helpers


class Index(object):
    """
    Build search index on a given knowledge base.

    - Create postings list
    - Keep track of articles ids and titles to be returned as search results
    """

    def __init__(self):
        """
        Initialize Index instance.
        """
        self.articles = {}
        self.postings = defaultdict(set)

        self.token_idf = {}

    def build_index(self, raw_content):
        """
        Read knowledge base and builds its search index.

        Args:
            raw_content (list[list[str]])
        """
        for article in raw_content:

            article_id, title, content = article

            tokens = preprocessing.tokenize(content)
            frequencies = preprocessing.count_frequency(tokens)

            for token in frequencies.keys():
                self.postings[token].add(article_id)

            self.articles[article_id] = Article(article_id=article_id,
                                                title=title,
                                                frequencies=frequencies)

    def calculate_tfidf(self):
        """
        Calculate tfidf vectors per aritcle.

        Since matrix is extremely sparse, we keep track of existing tokens and their
        tfidf values.
        """
        self._calculate_token_idf()
        for article_id, article in self.articles.iteritems():

            for token, frequency in article.frequencies.iteritems():
                self.articles[article_id].add_tfidf(token, float(frequency) * float(self.token_idf[token]))

            # no longer needed, save memory while writing
            self.articles[article_id].clear_freq()

    def _calculate_token_idf(self):
        """
        Calculate token idf to aid the calculation of tfidf vectors.
        """
        total_articles = len(self.articles)

        for token in self.postings:
            total_docs_with_token = len(self.postings[token])
            self.token_idf[token] = log(
                float(total_articles) / float(total_docs_with_token))

    def get_data(self):
        """
        Return data used for searching.

        Return
            dict{str:dict}: all dictionaries needed to perform search
        """
        return {'postings': self.postings,
                'articles': self.articles,
                'idf': self.token_idf}

    def save(self, path_to_dir):
        """
        Save necessary information for building the index.

        Args:
            path_to_dir (str)
        """
        data = self.get_data()

        articles_as_chunks = helpers.split_dict(data['articles'], 10)

        for i in xrange(len(articles_as_chunks)):
            data['article_%i' % (i + 1)] = articles_as_chunks[i]

        data.pop('articles')

        io.write_batch(data, path_to_dir, '.pkl')

    def load(self, path_to_index_dir):
        """
        Load existing index.

        Args:
            path_to_index(str)
        """
        for file in os.listdir(path_to_index_dir):

            abs_path = '%s/%s' % (path_to_index_dir, file)

            if 'article' in file:
                self.articles.update(io.read(abs_path))

            elif 'postings' in file:
                self.postings = io.read(abs_path)

            elif 'idf' in file:
                self.token_idf = io.read(abs_path)
