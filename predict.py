from core.STFT.STFTMusicProcessorPredict import STFTMusicProcessorPredict
from database.MySQLConnector import MySQLConnector
from utils.hparam import hp
import os
from utils.print_utils import print_error, print_message, print_warning


def predict():
    connector = MySQLConnector()
    music_processor = STFTMusicProcessorPredict()

    for path in os.listdir(hp.fingerprint.path.query_path):

        try:
            music_path = os.path.join(hp.fingerprint.path.query_path, path)
            music_info = music_processor.predict_music(music_path=music_path, connector=connector)
            print_message("Bài hát được dự đoán: " + str(music_info['music_id']) + ", --- Số lượng Hash khớp：" + str
            (music_info['max_hash_count']) + ", --- phần khớp bài hát：" + str(music_info['music_offset']))
            pass
        except BaseException as e:
            print_error("Error: " + str(path) + "\n" + str(e))
            continue
        pass
    pass


if __name__ == '__main__':
    predict()
