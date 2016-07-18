"""
Contains the Index class.
"""
from collections import namedtuple
from collections import defaultdict
from math import log

from my_search.util import preprocessing

Article = namedtuple('Article', ['article_id', 'title', 'frequencies'])


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
        self.article_tfidf = {}

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

    def calculate_tfdf(self):
        """
        Calculate tfidf vectors per aritcle.

        Since matrix is extremely sparse, we keep track of existing tokens and their
        tfidf values.
        """
        self._calculate_token_idf()
        for article_id, article in self.articles.iteritems:
            for token, frequency in article.frequencies.iteritems():
                self.article_tfidf[article_id][
                    token] = float(frequency) * float(self.token_idf[token])

    def _calculate_token_idf(self):
        """
        Calculate token idf to aid the calculation of tfidf vectors.
        """
        total_articles = len(self.articles)

        for token in self.postings:
            total_docs_with_token = len(self.postings[token])
            self.token_idf[token] = log(
                float(total_articles) / float(total_docs_with_token))
