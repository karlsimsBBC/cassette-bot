import argparse

from cassettebot.builder import VideoBuilder
from cassettebot.composer import ScriptComposer
from cassettebot.exceptions import InputError

def main():
    args = parse_args()
    builder = VideoBuilder()
    composer = ScriptComposer()
    try:
        new_transcript = composer.compose(args.product, args.transcript, args.input_text)
        if args.verbose and composer.inspect(new_transcript):
            return
        builder.build(new_transcript, args.video_source, args.video_output)
    except InputError as e:
        print(f'{InputError.__name__}:\n\t{e}')

def parse_args():
    parser = argparse.ArgumentParser('Cassette Bot')
    parser.add_argument(
        'product',
        metavar='PRODUCT',
        type=str,
        choices=('speech', 'silence', 'markov'),
        help='type of product: \n\t{\'speech\', \'silence\', \'markov\'}')
    parser.add_argument(
        'video_source',
        type=str,
        help='path of video to process')
    parser.add_argument(
        'transcript',
        type=str,
        help='path of timecoded json transcript')
    parser.add_argument(
        '--input_text',
        '-i',
        type=str,
        help='input text',
        default='')
    parser.add_argument(
        '--video_output', '-o',
        type=str,
        help='output directory path',
        default='video.mp4')
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        default=False)
    return parser.parse_args()

if __name__ == '__main__':
    main()