import unittest
from collections import namedtuple

from my_search.util import preprocessing

TestCase = namedtuple('TestCase', ['input', 'expected'])


tokenizing_cases = [TestCase(input='Well, here is a START.',
                             expected=['well', 'here', 'is', 'a', 'start']),

                    TestCase(input='Testing this- out',
                             expected=['testing', 'this', 'out']),

                    TestCase(input='',
                             expected=[''])]


class TestPreprocessing(unittest.TestCase):

    def test_tokenize(self):
        for case in tokenizing_cases:
            output = preprocessing.tokenize(case.input)
            self.assertEqual(output, case.expected)

    def text_counting_frequencies(self):
        expected = {'portugal': 3,
                    'ronaldo': 2,
                    'europe': 1}

        input = ['portugal', 'ronaldo', 'europe', 'portugal', 'ronaldo']

        output = preprocessing.count_frequency(input)

        self.assertDictEqual(output, expected)
