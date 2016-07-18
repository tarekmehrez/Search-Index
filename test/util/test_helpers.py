import unittest
from collections import namedtuple
from nose.tools import raises

from my_search.util import helpers
from my_search.exceptions import QueryTooLongException


TestCase = namedtuple('TestCase', ['input', 'expected'])

vectors = {'x': {1: 1, 2: 2, 3: 3},
           'y': {1: 10, 2: 20, 3: 30},
           'z': {1: 100, 2: 200}}


class TestHelpers(unittest.TestCase):

    def test_cosine_sim_x_y(self):
        expected = 0.0
        output = helpers.cosine_similarity(vectors['y'], vectors['x'])
        self.assertAlmostEqual(output, expected, places=3)

    def test_cosine_sim_z_x(self):
        expected = 0.93
        output = helpers.cosine_similarity(vectors['z'], vectors['x'])
        self.assertAlmostEqual(output, expected, places=3)

    @raises(QueryTooLongException)
    def test_cosine_sim_x_z(self):
        helpers.cosine_similarity(vectors['x'], vectors['z'])
