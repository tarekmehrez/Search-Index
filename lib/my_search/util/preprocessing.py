"""
Contains the preprocessing module.
"""
import string
import re

from collections import defaultdict


# TODO:
# stop word removal
# lemmatization

def tokenize(text):
    """
    Take in a piece of text, process and tokenize it.

    Args:
        text (str)
    Returns
       list[str]: tokenized text
    """
    # strip punctiations
    text = text.translate(string.maketrans("", ""), string.punctuation)

    # multiple spaces to one
    text = re.sub('[\s]+', ' ', text)

    # lower case
    text = text.lower()

    # now tokenize
    return text.split(' ')


def count_frequency(tokens):
    """
    Count tokens frequency.

    Args:
        list[str]: tokens
    Returns
        dict{str:int}: each token and its count
    """
    frequencies = defaultdict(int)

    for token in tokens:
        frequencies[token] += 1

    return frequencies
