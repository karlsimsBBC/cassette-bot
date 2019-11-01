import unittest
import random

from cassettebot.markov import Markov
from test.utils import load_fixture

random.seed(0)

class TestMarkov(unittest.TestCase):

    with open('test/fixtures/document.txt') as fp:
        document = fp.read()

    def test_build_chain(self):
        markov = Markov('Our Father in heaven, hallowed be your name', 2)
        actual = dict(markov.chain)
        expected = {
            '<s> <s>':     ['our'],
            '<s> our':     ['father'],
            'our father':  ['in'],
            'father in':   ['heaven'],
            'in heaven':   [','],
            'heaven ,':    ['hallowed'],
            ', hallowed':  ['be'],
            'hallowed be': ['your'],
            'be your':     ['name']
        }
        self.assertEqual(actual, expected)

    def test_generate(self):
        markov = Markov(self.document)
        actual = markov.generate(seed='the british people', minlen=10)
        expected = 'the british people . and , yes . let\'s start now on those free trade deals ,'
        self.assertEqual(actual, expected)
    