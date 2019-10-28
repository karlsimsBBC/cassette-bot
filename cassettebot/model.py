import collections


class Model(object):

    def __init__(self, data: dict):
        words = data['words'] + [EOF]
        self.wordset = self.model_wordset(words)
        self.instances = self.model_instances(words)

    def model_wordset(self, words: list) -> dict:
        wordset = collections.defaultdict(list)
        for i, word in enumerate(words):
            wordset[word['word']].append(i)
        return dict(wordset)
        
    def model_instances(self, words: list) -> list:
        return [self.link_next(words, i) for i in range(len(words)-1)]

    def link_next(self, words: list, i: int) -> dict:
        curr, peek = words[i], words[i+1]
        return dict(word=curr['word'],
                    start=curr['start'],
                    end=curr['end'],
                    next=peek['word'], 
                    next_index=i+1)


EOF = {'word': '<EOF>'}