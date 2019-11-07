# Cassette Bot

🤖 📼 Commandline tool for remixing videos with timecoded transciptions.

## Requirements
**[ffmpeg](https://www.ffmpeg.org/)** (A complete, cross-platform solution to record, convert and stream audio and video)
```bash
$ brew install ffmpeg
```

## Installation

```
make build
```

Or to build with examples:
```
make build_with_examples
```

## Workflows

### Speech
Produce a video spliced to match the `input_text`. 
```bash
$ cassettebot speech \
    examples/mark/video.mp4 \
    examples/mark/transcription.json \
    --input_text='i wanna talk about this specific situation when i was in college and I started facebook' \
    --video_output='examples/mark/results/speech.mp4' \
    --verbose
```
See result: `examples/results/speech.mp4`

### Silence
Produce a video from the original with all speech instances removed.
```bash
$ cassettebot silence \
    examples/mark/video.mp4 \
    examples/mark/transcription.json \
    --video_output='examples/mark/results/silence.mp4'
```
See result: `examples/results/silence.mp4`

### General Use
```bash
usage: Cassette Bot [-h] [--input_text INPUT_TEXT]
                    [--video_output VIDEO_OUTPUT] [--verbose]
                    {speech,silence,markov} video_source transcript

positional arguments:
  {speech,silence,markov}
                        type of product: {'speech', 'silence', 'markov'}
  video_source          path of video to process
  transcript            path of timecoded json transcript

optional arguments:
  -h, --help            show this help message and exit
  --input_text INPUT_TEXT, -i INPUT_TEXT
                        input text
  --video_output VIDEO_OUTPUT, -o VIDEO_OUTPUT
                        output directory path
  --verbose, -v         check created transcript before building video
```

🤖 📼 **Pull requests welcome**