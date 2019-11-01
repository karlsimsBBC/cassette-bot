import json
import textwrap

from cassettebot.model import Model
from cassettebot.silence import Silence
from cassettebot.speech import Speech
from cassettebot.exceptions import InputError

class ScriptComposer(object):

    def compose(self, product: str, transcript: str, text: str) -> dict:
        try:
            with open(transcript) as fp:
                data = json.load(fp)
        except json.JSONDecodeError:
            raise InputError(f'Unable to decode JSON in transcipt: \'{transcript}\'')
        except FileNotFoundError:
            raise InputError(f'No such transcipt file: \'{transcript}\'')
        # get function from within the class
        product_func = getattr(self, f'{product}_script')
        return product_func(data, text)

    def silence_script(self, transcript, text) -> dict:
        composer = Silence(transcript)
        return composer.compose()

    def speech_script(self, transcript, text) -> dict:
        composer = Speech(transcript)
        if not text:
            raise InputError(f'Cannot generate speech with empty input text')
        return composer.compose(text)
    
    def inspect(self, transcript) -> bool:
        phrases = transcript['phrases']
        text = transcript['text']
        total_clips = len(phrases)
        skipped_words = [w['text'][1:-1] for w in phrases if w['text'].startswith('[')]
        print('-' * 70)
        print('\n  '.join(['Generated script:\n'] + textwrap.wrap(text)), end='\n\n')
        print('skipped:', ' '.join(skipped_words))
        return input('continue ? [Y/n]: ') != 'y'
