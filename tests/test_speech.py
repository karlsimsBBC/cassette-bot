import unittest

from cassettebot.composer import Speech
from cassettebot.exceptions import InputError
from tests.utils import load_fixture


class TestSpeech(unittest.TestCase):

    maxDiff = None

    document = load_fixture('kaldi_doc.json')
    empty_document = load_fixture('kaldi_empty_doc.json') 
    number_document = load_fixture('number_doc.json')

    def test__init__empty_dataset(self):
        with self.assertRaises(InputError) as context:
            composer = Speech(self.empty_document)
            self.assertEqual('no speech instances given', context.exception)

    def test_find_single_phrase(self):
        composer = Speech(self.document)
        actual = composer.compose('over the hills and far away')
        expected = {
            'text': 'over the hills and far away',
            'phrases': [
                {'text': 'over the hills and far away', 'start': 34.38, 'end': 36.44}
            ]
        }
        self.assertEqual(actual, expected)

    def test_find_with_missing_word(self):
        composer = Speech(self.document)
        actual = composer.compose('over the cliffs and far away')
        expected = {
            'text': 'over the | [cliffs] | and far away',
            'phrases': [
                {'text': 'over the','start': 34.38,'end': 34.79},
                {'text': '[cliffs]', 'start': 13.59, 'end': 14.13},
                {'text': 'and far away', 'start': 35.31, 'end': 36.44}
            ]
        }
        self.assertEqual(actual, expected)

    def test_find_single(self):
        composer = Speech(self.document)
        actual = composer.compose('away')
        expected = {
            'text': 'away',
            'phrases': [
                {'text': 'away', 'start': 35.88, 'end': 36.44}
            ]
        }
        self.assertEqual(actual, expected)

    def test_find_with_wildcards(self):
        composer = Speech(self.document)
        composer = Speech(self.document)
        actual = composer.compose('over * hills * * away')
        expected = {
            'text': 'over the hills and far away',
            'phrases': [
                {'text': 'over the hills and far away', 'start': 34.38, 'end': 36.44}
            ]
        }
        self.assertEqual(actual, expected)

    def test_find_with_wildcard_at_start(self):
        composer = Speech(self.document)
        actual = composer.compose('* the hills * far away')
        expected = {
            'text': 'over the hills and far away',
            'phrases': [
                {'text': 'over the hills and far away', 'start': 34.38, 'end': 36.44}
            ]
        }
        self.assertEqual(actual, expected)

    def test_find_with_gaps(self):
        composer = Speech(self.document)
        actual = composer.compose('oh and a a over the hills and far away')
        expected = {
            'text': 'oh and a a | over the hills and far away',
            'phrases': [
                {'text': 'oh and a a', 'start': 13.59, 'end': 16.09},
                {'text': 'over the hills and far away', 'start': 34.38, 'end': 36.44}
            ]
        }
        self.assertEqual(actual, expected)

    def test_find_with_number_match(self):
        composer = Speech(self.number_document)
        actual = composer.compose('more than %d businesses')
        expected = {
            'text': 'more than seventy million businesses',
            'phrases': [
                {'text': 'more than seventy million businesses', 'start': 34.38, 'end': 35.49}
            ]
        }
        self.assertEqual(actual, expected)

    def test_find_empty_str(self):
        composer = Speech(self.document)
        actual = composer.compose('')
        expected = {'text': '', 'phrases': []}
        self.assertEqual(actual, expected)

    def test_linked_words(self):
        composer = Speech(self.document)
        composer.tokens = ['over', 'the', 'hills', 'and', 'far', 'away']
        word = composer.wordset['over'][0]
        actual = composer.linked_words(word, 0)
        expected = [4, 5, 6, 7, 8, 9]
        self.assertEqual(actual, expected)