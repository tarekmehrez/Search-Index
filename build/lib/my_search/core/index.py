"""
Contains the Index class.
"""
from collections import namedtuple
from collections import defaultdict

from my_search.util import preprocessing

Article = namedtuple('Article', ['title', 'article_id'])


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
        self.total_counts = defaultdict(int)
        self.articles = {}
        self._ostings = defaultdict(lambda: defaultdict(int))

    def build_index(self, raw_content):
        """
        Read knowledge base and builds its search index.

        Args:
            raw_content (list[list[str]])
        """
        for article in raw_content:

            article_id, title, content = article
            self.articles[article_id] = Article._make(article_id, title)

            tokens = preprocessing.tokenize(content)
            frequencies = preprocessing.count_frequency(tokens)

            for token in tokens:
                count = frequencies[token]

                self.total_counts[token] += count
                self.postings[token][article_id] = count
