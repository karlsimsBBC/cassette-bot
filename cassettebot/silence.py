

class Silence(object):

    def __init__(self, transcript: dict, minlen=1.0, inset=0.2):
        self.transcript = transcript
        self.minlen = minlen
        self.inset = inset
    
    def find(self) -> list:
        last = 0.0
        instances = []
        for word in self.transcript['words']:
            if self.has_pause(last, word['start']):
                instances.append(self.instance(last, word['start']))
            last = word['end']
        return dict(text='Silence...', phrases=instances)

    def has_pause(self, a: float, b: float) -> bool: 
        return abs(a - b) >= self.minlen

    def instance(self, start: float, end: float) -> dict:
        return dict(text='<PAUSE>', 
                    start=round(start + self.inset, 2),
                    end=round(end - self.inset, 2))