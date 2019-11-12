import os

from cassettebot.composer.model import Model
from cassettebot.exceptions import InputError


with open('cassettebot/resources/numbers') as fp:
    NUMBERS = set(fp.read().split())


class Speech(object):

    def __init__(self, transcript: dict, skip=None, model_class=Model, min_pause=2.0):
        model = model_class(transcript)
        if len(model.instances) <= 0:
            raise InputError('no speech instances given')
        self.wordset = model.wordset
        self.instances = model.instances
        self.min_pause = min_pause
        self.skip = skip or (lambda w: dict(self.instances[0], word=f'[{w}]'))

    def compose(self, text: str) -> dict:
        phrases = self.find(text)
        return dict(phrases=phrases, text=' | '.join(p['text'] for p in phrases))
    
    def find(self, text: str) -> list:
        return [self.merge(words) for words in self.find_phrases(text)]

    def merge(self, words: list) -> dict:
        return dict(start=words[0]['start'], 
                    end=words[-1]['end'],
                    text=cat(w['word'] for w in words))

    def find_phrases(self, text: str) -> list:
        self.tokens = text.lower().split()
        self.index = -1
        curr = self.next_token()
        phrases = []
        while curr:
            choice = self.longest_word_chain(curr, self.index)
            phrases.append(choice)
            curr = self.next_token(len(choice))
        return phrases
        
    def longest_word_chain(self, curr: str, i: int) -> list:
        if curr == '*':
            choices = range(len(self.instances) - 1)
        else:
            choices = self.wordset.get(curr, [])
        if not choices:
            return [self.skip(curr)]
        choice = max((self.linked_words(w, i) for w in choices), key=len)
        return [self.instances[index] for index in choice]

    def linked_words(self, start: int, pos: int) -> list:
        path = [start]
        while pos < len(self.tokens) - 1:
            pos += 1
            node = self.instances[path[-1]]
            next_node = self.instances[node['next_index']]
            if not self.match(self.tokens[pos], next_node['word']):
                return path
            if self.has_pause(node['end'], next_node['start']):
                return path
            path.append(node['next_index'])
            # TODO: ignore connections with more than a second pause
        return path

    def match(self, token: str, next_word: str) -> bool:
        'match next token with next node or accept if wildcard'
        if token in (next_word, '*'):
            return True
        if token == '%d':
            return self.match_number(next_word)
        return False

    def match_number(self, next_word: str) -> bool:
        return next_word in NUMBERS

    def has_pause(self, a: float, b: float) -> bool: 
        return abs(a - b) >= self.min_pause
        
    def next_token(self, inc=1) -> str:
        if self.index + inc >= len(self.tokens):
            return None
        self.index += inc
        return self.tokens[self.index]


cat = ' '.join
