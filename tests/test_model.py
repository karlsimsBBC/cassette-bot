import unittest

from cassettebot.composer import Model
from tests.utils import load_fixture


class TestModel(unittest.TestCase):

    document = load_fixture('kaldi_small_doc.json')
    empty_document = load_fixture('kaldi_empty_doc.json')
    
    def test_model_wordset(self):
        model = Model(self.document)
        actual = model.wordset
        expected = {'oh': [0], 'and': [1], 'a': [2, 3], 'over': [4],'<EOF>': [5]}
        self.assertEqual(actual, expected)

    def test_model_instances(self):
        model = Model(self.document)
        actual = model.instances
        expected = [
            {'next': 'and', 'next_index': 1, 'start': 13.59, 'end': 14.13, 'word': 'oh'},
            {'next': 'a', 'next_index': 2, 'start': 14.13, 'end': 14.64, 'word': 'and'},
            {'next': 'a', 'next_index': 3, 'start': 14.9, 'end': 15.6, 'word': 'a'},
            {'next': 'over', 'next_index': 4, 'start': 16.01, 'end': 16.09, 'word': 'a'},
            {'next': '<EOF>', 'next_index': 5, 'start': 34.38, 'end':  34.7, 'word': 'over'}
        ]
        self.assertEqual(actual, expected)

    def test_model_wordset_empty(self):
        model = Model(self.empty_document)
        actual = model.wordset
        expected = {'<EOF>': [0]}
        self.assertEqual(actual, expected)
        
    def test_model_instances(self):
        model = Model(self.empty_document)
        actual = model.instances
        expected = []
        self.assertEqual(actual, expected)
    
