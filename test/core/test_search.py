import unittest
from collections import namedtuple

from my_search.core import SearchEngine
from my_search.core import Index


CONTENT = [['123', 'football', 'portugal ronaldo europe europe'],
           ['234', 'portugal', 'Lisbon, Porto, Portugal porto'],
           ['456', 'europe', 'Europe, France, Portugal portugal france']]


NUM_OF_RESULTS = 3

TestCase = namedtuple('TestCase', ['input', 'expected'])

search_cases = [
    TestCase(input='portugal', expected=[
             ('234', 'portugal'), ('123', 'football'), ('456', 'europe')]),
    TestCase(input='europe', expected=[
             ('123', 'football'), ('456', 'europe')]),
    TestCase(input='', expected=[]),
    TestCase(input='wrong query', expected=[])]


class TestSearchEngine(unittest.TestCase):

    def setUp(self):
        self.engine = SearchEngine()

        index = Index()
        index.build_index(CONTENT)
        index.calculate_tfidf()

        self.engine.index = index

    def test_search(self):
        for case in search_cases:
            results = self.engine.search(case.input, NUM_OF_RESULTS)
            self.assertListEqual(results, case.expected)
