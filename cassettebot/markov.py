import re
import random
import collections


class Markov(object):

    def __init__(self, text: str, n=3):
        self.n = n
        self.chain = self.build_chain(text, n)

    def build_chain(self, text: str, n: int) -> dict:
        chain = collections.defaultdict(list)
        prefix = ['<s>'] * self.n
        for t in self.tokenise(text):
            chain[cat(prefix)].append(t)
            prefix = prefix[1:] + [t]
        return chain

    def generate(self, seed=None, minlen=32):
        seed = self.tokenise(seed or random.choice(list(self.chain.keys())))
        prefix = seed[-self.n:]
        assert len(prefix) >= self.n, f'Seed too short. Need >= {self.n}'
        return cat(self._generate(seed, prefix, minlen))

    def _generate(self, words: list, prefix: list, minlen: int) -> list:
        (i, s) = (0, '')
        while i < minlen or s not in delimeters:
            choices = self.chain[cat(prefix)]
            if not choices:
                break
            s = random.choice(choices)
            words.append(s)
            prefix = prefix[1:] + [s]
            i += 1
        return words

    def tokenise(self, text: str) -> list:
        return tokeniser.findall(text.lower())
    

tokeniser  = re.compile(r'[\w\'a-zA-ZÀ-ÖØ-öø-ÿ]+|[.,!?\";]')
delimeters = frozenset('.,!?;')


cat = ' '.join