import json
import textwrap

from cassettebot.model import Model
from cassettebot.silence import Silence
from cassettebot.speech import Speech
from cassettebot.markov import Markov
from cassettebot.exceptions import InputError


class ScriptComposer(object):

    def compose(self, product: str, transcript_file: str, text: str) -> dict:
        try:
            data = json.loads(transcript_file.read())
        except json.JSONDecodeError:
            raise InputError(f'Unable to decode JSON in transcipt: \'{transcript}\'')
        # get function from within the class
        product_func = getattr(self, f'{product}_script')
        return product_func(data, text)

    def silence_script(self, transcript: dict, text: str) -> dict:
        composer = Silence(transcript)
        return composer.compose()

    def speech_script(self, transcript: dict, text: str) -> dict:
        composer = Speech(transcript)
        if not text:
            raise InputError(f'Cannot generate speech with empty input text')
        return composer.compose(text)

    def markov_script(self, transcript: dict, text: str) -> dict:
        corpus = transcript.get('punct', transcript.get('text', None))
        if not corpus:
            raise InputError(f'Cannot generate markov without trancript text')
        markov = Markov(corpus)
        composer = Speech(transcript)
        return composer.compose(markov.generate(text))

    def inspect(self, transcript: dict) -> bool:
        phrases = transcript['phrases']
        text = transcript['text']
        total_clips = len(phrases)
        skipped_words = [w['text'][1:-1] for w in phrases if w['text'].startswith('[')]
        print('-' * 70)
        print('\n  '.join(['Generated script:\n'] + textwrap.wrap(text)), end='\n\n')
        print('skipped:', ' '.join(skipped_words))
        return input('continue ? [Y/n]: ') != 'y'
