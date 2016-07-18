import unittest
from collections import defaultdict

from my_search.core import Index

DECIMAL_PLACES = 2

CONTENT_AS_LIST = [['123', 'football', 'portugal ronaldo europe europe'],
                   ['234', 'portugal', 'Lisbon, Porto, Portugal porto'],
                   ['456', 'Europe', 'Europe, France, Portugal portugal france']]


CONTENT_AS_POSTINGS = defaultdict(set, {'europe': {'123', '456'},
                                        'france': {'456'},
                                        'lisbon': {'234'},
                                        'porto': {'234'},
                                        'portugal': {'123', '234', '456'},
                                        'ronaldo': {'123'}})

TOKEN_IDFs = {'europe': 0.41,
              'france': 1.10,
              'lisbon': 1.10,
              'porto': 1.10,
              'portugal': 0.0,
              'ronaldo': 1.10}

TFIDFs = {'234':
            {'porto': 2.20,
             'portugal': 0.0,
             'lisbon': 1.10},

         '123':
            {'europe': 0.81,
             'ronaldo': 1.10,
             'portugal': 0.0},

         '456':
            {'europe': 0.41,
             'portugal': 0.0,
             'france': 2.20}}


class TestIndex(unittest.TestCase):

    def setUp(self):
        self.index = Index()
        self.index.build_index(CONTENT_AS_LIST)

    def test_build_index(self):
        self.index.build_index(CONTENT_AS_LIST)
        self.assertDictEqual(self.index.postings, CONTENT_AS_POSTINGS)

    def test_calculating_idf(self):
        self.index._calculate_token_idf()

        for token in self.index.token_idf:
            output = round(self.index.token_idf[token], DECIMAL_PLACES)
            excepted = TOKEN_IDFs[token]
            self.assertAlmostEqual(output, excepted)

    def test_calculating_tfidf(self):
        self.index.calculate_tfidf()

        for article_id, article in self.index.articles.iteritems():
            for token, tfidf_value in article.tfidf.iteritems():
                output = round(tfidf_value, DECIMAL_PLACES)
                expected = TFIDFs[article_id][token]

                self.assertAlmostEqual(output, expected)
