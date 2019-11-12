import collections


class Model(object):

    def __init__(self, data: dict):
        self.words = data['words'] + [EOF]
        self.wordset = self.model_wordset()
        self.instances = self.model_instances()

    def model_wordset(self) -> dict:
        wordset = collections.defaultdict(list)
        for i, word in enumerate(self.words):
            wordset[word['word']].append(i)
        return dict(wordset)
        
    def model_instances(self) -> list:
        return [self.link_next(i) for i in range(len(self.words)-1)]

    def link_next(self, i: int) -> dict:
        (curr, peek) = (self.words[i], self.words[i+1])
        return dict(word=curr['word'],
                    start=curr['start'],
                    end=curr['end'],
                    next=peek['word'], 
                    next_index=i+1)


EOF = {'word': '<EOF>'}
