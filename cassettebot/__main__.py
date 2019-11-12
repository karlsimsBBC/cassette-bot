from cassettebot.composer import ScriptComposer
from cassettebot.builder import VideoBuilder
from cassettebot.exceptions import InputError
from cassettebot.argparser import parse_args


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

if __name__ == '__main__':
    main()
