import subprocess

from cassettebot.exceptions import InputError


class VideoBuilder(object):

    def build(self, transcript: dict, video_source: str, video_output: str):
        'build video from generated transcript'
        phrases = transcript['phrases']
        timecodes = self.compile_timecodes(phrases)
        options = [
            'ffmpeg',
            '-i', video_source,
            '-filter_complex', timecodes,
            '-map', '[out]',
            video_output
        ]
        subprocess.call(options)

    def compile_timecodes(self, phrases: list) -> str:
        'compile phrases to ffmpeg slice and concat instructions'
        if len(phrases) == 0:
            raise InputError('Empty phrase list, cannot compile timecodes')
        components = [
            *self.compile_slices(phrases),
            *self.compile_concatination(phrases)
        ]
        return cat(components)

    def compile_slices(self, phrases: list) -> iter:
        'compiles ffmpeg slice instructions'
        video_clip = '[0:v]trim={start}:{end},setpts=PTS-STARTPTS[v{index}];'
        audio_clip = '[0:a]atrim={start}:{end},asetpts=PTS-STARTPTS[a{index}];'
        for i, phrase in enumerate(phrases):
            yield video_clip.format(index=i, **phrase)
            yield audio_clip.format(index=i, **phrase)

    def compile_concatination(self, phrases: list) -> list:
        'compiles ffmpeg concat instructions'
        meta_clip = '[v{index}][a{index}]'
        concat_info = 'concat=n={total}:v=1:a=1[out]'
        total = len(phrases)
        orderings = [meta_clip.format(index=i) for i in range(total)]
        for i in range(total):
            yield meta_clip.format(index=i)
        yield concat_info.format(total=total)


cat = ''.join
