import unittest

from cassettebot.silence import Silence
from test.utils import load_fixture


class TestSilence(unittest.TestCase):
    
    document = load_fixture('kaldi_small_doc.json')
    empty_document = load_fixture('kaldi_empty_doc.json') 

    def test_find(self):
        composer = Silence(self.document)
        actual = composer.find()
        expected = {
            'text': 'Silence...',
            'phrases': [
                {'text': '<PAUSE>', 'start': 0.2, 'end': 13.39},
                {'text': '<PAUSE>', 'start': 16.29, 'end': 34.18}
            ]
        }
        self.assertEqual(actual, expected)

    def test_find_empty(self):
        composer = Silence(self.empty_document)
        expected = {
            'text': 'Silence...',
            'phrases': []
        }
        actual = composer.find()
        self.assertEqual(actual, expected)