import os
from utils.print_utils import print_error, print_message, print_warning
from database.MySQLConnector import MySQLConnector
from core.STFT.STFTMusicProcessorCreate import STFTMusicProcessorCreate


def create_database():

    connector = MySQLConnector()
    music_processor = STFTMusicProcessorCreate()
    # duong dan den folder chua nhac
    # music_path = "./dataset"
    for path in os.listdir(music_path): 
        print(path)
        try:
            music_path = os.path.join(music_path, path) 
            music_processor.create_finger_prints_and_save_database(
                music_path=music_path, connector=connector)

        except BaseException as e:
            print_error("Error: " + str(path) + "\n" + str(e))
            continue
        pass
    pass


if __name__ == '__main__':
    create_database()