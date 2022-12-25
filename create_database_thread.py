import os
from utils.hparam import hp
from utils.print_utils import print_error, print_message, print_warning
from database.MySQLConnector import MySQLConnector
from core.STFT.STFTMusicProcessorCreate import STFTMusicProcessorCreate
import threading
import numpy as np


class MyThread(threading.Thread):

    def __init__(self, all_path):
        super(MyThread, self).__init__()
        self.all_path = all_path
        pass

    def run(self) -> None:
        create_database(self.all_path)
        pass

    pass


def create_database(all_path):
    # Get the connection to the database
    connector = MySQLConnector()

    # Processing of short-time Fourier transform
    music_processor = STFTMusicProcessorCreate()

    # Get the path to the song
    for path in all_path:

        try:
            # Get the path of the song
            # music_path = os.path.join(hp.fingerprint.path.music_path, path)
            music_path = path
            # Create a fingerprint and save it to the database
            music_processor.create_finger_prints_and_save_database(
                music_path=music_path,
                connector=connector
            )
        # exception handling
        except BaseException as e:
            print_error("Error: " + str(path) + "\n" + str(e))
            continue

        print_message("Created！！！")

        pass

    pass


if __name__ == '__main__':
    # Get the full path of the song
    path_list = []
    print(hp.fingerprint.path.music_path)
    for path in os.listdir(hp.fingerprint.path.music_path):
        path = os.path.join(hp.fingerprint.path.music_path, path)
        path_list.append(path)

    # Divide the contents of the list into 3 equal parts
    path_list = np.array_split(path_list, hp.fingerprint.thread_num)

    # Thread Pool
    thread_list = []
    # Start threads one by one
    for path in path_list:
        t = MyThread(path)
        thread_list.append(t)

    for thread_ in thread_list:
        thread_.run()
