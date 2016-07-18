"""
Contains io module.
"""

import os
import csv
import cPickle

from my_search.exceptions import FormatNotSupportedException

SUPPORTED_READ_EXTENSIONS = ['.tsv', '.pkl']
SUPPORTED_WRITE_EXTENSIONS = ['.pkl']

# TODO: handle encoding


def exists(file_path):
    """
    Check if path exists.

    Args:
        file_path (str): path to the file to be checked
    Returns:
        bool: whether it exists or not
    """
    return os.path.exists(file_path)


def read(file_path):
    """
    Check extension, calls respective read function.

    Args:
        file_path (str): path to the file to be read
    """
    _, extension = os.path.splitext(file_path)

    if extension not in SUPPORTED_READ_EXTENSIONS:
        raise FormatNotSupportedException(
            'Cant read file with %s format' % extension)

    if extension == '.tsv':
        return _read_tsv(file_path)

    if extension == '.pkl':
        return _read_pkl(file_path)


def _read_tsv(file_path):
    """
    Read tsv files.

    Args:
        file_path (str): path to the file to be read
    Returns:
        list[list(str)]: content of the tsv file
    """
    with open(file_path) as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        content = [row for row in reader]

    return content


def _read_pkl(file_path):
    """
    Read pkl files.

    Args:
        file_path (str): path to the file to be read
    Returns:
        obj: content of the pkl file
    """
    with open(file_path, 'rb') as f:
        content = cPickle.load(f)

    return content


def write(content, file_path):
    """
    Check extension, calls respective write function.

    Args:
        content (obj): content of the file to be written
        file_path (str): path to the output file
    """
    _, extension = os.path.splitext(file_path)
    if extension not in SUPPORTED_WRITE_EXTENSIONS:
        raise FormatNotSupportedException(
            'Cant write file with %s format' % extension)

    if extension == '.pkl':
        return _write_pkl(content, file_path)


def _write_pkl(content, file_path):
    """
    Write content to a pkl format.

    Args:
        content (obj): content of the file to be written
        file_path (str): path to the output file
    """
    with open(file_path, 'wb') as f:
        cPickle.dump(content, f, protocol=cPickle.HIGHEST_PROTOCOL)
