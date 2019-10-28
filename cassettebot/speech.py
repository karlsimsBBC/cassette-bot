from cassettebot.model import Model
from cassettebot.exceptions import InputError

class Speech(object):

    def __init__(self, transcript: dict, skip=None, model_class=Model):
        model = model_class(transcript)
        if len(model.instances) <= 0:
            raise InputError('no speech instances given')
        self.wordset = model.wordset
        self.instances = model.instances
        self.skip = skip or (lambda w: dict(self.instances[0], word=f'[{w}]'))
    
    def find(self, text):
        self.tokens = text.lower().split()
        self.index = -1
        phrases = [self.merge(phrase) for phrase in self.chunk_phrases()]
        return dict(phrases=phrases, text=cat(p['text'] for p in phrases))

    def merge(self, phrase: list) -> dict:
        return dict(start=phrase[0]['start'], 
                    end=phrase[-1]['end'],
                    text=cat(w['word'] for w in phrase))

    def chunk_phrases(self) -> list:
        phrases = []
        curr = self.next_token()
        while curr:
            choice = self.longest_linked(curr, self.index)
            phrases.append(choice)
            curr = self.next_token(len(choice))
        return phrases
        
    def longest_linked(self, curr: str, i: int) -> list:
        choices = self.wordset.get(curr, [])
        if not choices:
            return [self.skip(curr)]
        choice = max((self.linked_words(w, i) for w in choices), key=len)
        return [self.instances[index] for index in choice]

    def linked_words(self, start: int, pos: int):
        path = [start]
        while pos < len(self.tokens) - 1:
            pos += 1
            node = self.instances[path[-1]]
            if node['next'] != self.tokens[pos]:
                return path
            path.append(node['next_index'])
            # TODO: ignore connections with more than a second pause
        return path
        
    def next_token(self, inc=1):
        if self.index + inc >= len(self.tokens):
            return None
        self.index += inc
        return self.tokens[self.index]


cat = ' '.join
