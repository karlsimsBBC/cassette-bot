import unittest

from cassettebot.builder import VideoBuilder
from cassettebot.exceptions import InputError

class TestVideoBuilder(unittest.TestCase):

    def test_compile_timecodes(self):
        builder = VideoBuilder()
        phrases = [
            {'text': 'hello', 'start': 0.0, 'end': 1.64},
            {'text': 'hello', 'start': 2.0, 'end': 3.50}
        ]
        actual = builder.compile_timecodes(phrases)
        expected = ('[0:v]trim=0.0:1.64,setpts=PTS-STARTPTS[v0];'
                    '[0:a]atrim=0.0:1.64,asetpts=PTS-STARTPTS[a0];' 
                    '[0:v]trim=2.0:3.5,setpts=PTS-STARTPTS[v1];'
                    '[0:a]atrim=2.0:3.5,asetpts=PTS-STARTPTS[a1];'
                    '[v0][a0][v1][a1]concat=n=2:v=1:a=1[out]')
        self.assertEqual(actual, expected)

    def test_compile_timecodes_single(self):
        builder = VideoBuilder()
        phrases = [
            {'text': 'hello', 'start': 0.0, 'end': 1.64}
        ]
        actual = builder.compile_timecodes(phrases)
        expected = ('[0:v]trim=0.0:1.64,setpts=PTS-STARTPTS[v0];'
                    '[0:a]atrim=0.0:1.64,asetpts=PTS-STARTPTS[a0];'
                    '[v0][a0]concat=n=1:v=1:a=1[out]')
        self.assertEqual(actual, expected)

    def test_compile_timecodes_empty(self):
        builder = VideoBuilder()
        phrases = []
        with self.assertRaises(InputError) as context:
            builder.compile_timecodes(phrases)
            self.assertEqual('Empty phrase list, cannot compile timecodes', context.exception)