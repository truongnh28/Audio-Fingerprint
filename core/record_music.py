import argparse
from argparse import RawTextHelpFormatter
from core.listener import Listener


# Listen to music clips recorded by other devices and save them in the dataset/record_music directory
def get_audio():
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-s', '--seconds', nargs='?')
    args = parser.parse_args()

    if not args.seconds:
        args.seconds = "7"

    seconds = int(args.seconds)

    chunk_size = 2 ** 12
    channels = 1
    record_forever = False

    listener = Listener()

    listener.start_recording(
        seconds=seconds,
        chunk_size=chunk_size,
        channels=channels
    )

    while True:
        buffer_size = int(listener.rate / listener.chunk_size * seconds)
        print("recording......")
        for i in range(0, buffer_size):
            number = listener.process_recording()

        if not record_forever: break

    print("Recording stopped...")
    listener.stop_recording()

    listener.save_recorded("../dataset/record_music/xxx.mp3")

    return './xxx.mp3'


path = get_audio()
print(path)
