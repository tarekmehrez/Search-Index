import unittest
import cPickle
import tempfile
from nose.tools import raises

from my_search.util import io
from my_search.exceptions import FormatNotSupportedException


CONTENT = ('123\tEU\tSo portugal won the EURO\n'
           '234\tPortugal\tyou should visit lisbon in portugal\n')

CONTENT_AS_LIST = [['123', 'EU', 'So portugal won the EURO'],
                   ['234', 'Portugal', 'you should visit lisbon in portugal']]


class TestIO(unittest.TestCase):

    def test_read_tsv(self):
        temp_file = tempfile.NamedTemporaryFile(suffix='.tsv', delete=True)

        with open(temp_file.name, mode='wb') as f:
            f.write(CONTENT)

        output = io.read(temp_file.name)

        self.assertListEqual(output, CONTENT_AS_LIST)

    def test_read_pkl(self):
        temp_file = tempfile.NamedTemporaryFile(suffix='.pkl', delete=True)

        with open(temp_file.name, mode='wb') as f:
            cPickle.dump(CONTENT, f)

        output = io.read(temp_file.name)

        self.assertEqual(output, CONTENT)

    @raises(FormatNotSupportedException)
    def test_read_tsv(self):
        temp_file = tempfile.NamedTemporaryFile(suffix='.txt', delete=True)
        io.read(temp_file.name)

    def test_write_to_pkl(self):
        temp_file = tempfile.NamedTemporaryFile(suffix='.pkl', delete=True)

        io.write(CONTENT, temp_file.name)
        output = io.read(temp_file.name)

        self.assertEqual(CONTENT, output)

    @raises(FormatNotSupportedException)
    def test_read_tsv(self):
        temp_file = tempfile.NamedTemporaryFile(suffix='.txt', delete=True)
        io.write(CONTENT, temp_file.name)
