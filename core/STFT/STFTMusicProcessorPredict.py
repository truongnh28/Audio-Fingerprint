import librosa
from core.ICore.IMusicProcessorPredict import IMusicProcessorPredict
from utils.hparam import hp
import numpy as np
from utils.data_utils import start_time, end_time
import matplotlib.pyplot as plt
import soundfile as sf


class STFTMusicProcessorPredict(IMusicProcessorPredict):

    # predict songs
    def predict_music(self, music_path, connector):
        # Calculate Hash
        hash = list(self._calculation_hash(music_path=music_path))

        # See if display time is enabled
        if hp.fingerprint.show_time:
            start = start_time()

        # Search in the database according to Hash, [hash, offset]
        match_hash_list = set(connector.find_math_hash(hashes=hash))

        if hp.fingerprint.show_plot.predict_plot.hash_plot:
            self._show_line_plot(match_hash_list)

        # See if display time is enabled
        if hp.fingerprint.show_time:
            end_time(start, 'Time spent looking up in the database')

        return self._align_match(match_hash_list=match_hash_list)

    # matching core
    def _align_match(self, match_hash_list):
        # The fingerprint to be checked corresponds to the song id in the database,
        # the offset of the fingerprint to be checked in the database, and the offset of the fingerprint to be checked
        # in the music segment to be checked

        # The final returned song id
        music_id = -1
        # The offset of the final returned song
        music_offset = -1
        # The number of hashes that are found to match are finally returned
        max_hash_count = -1

        # save the returned result
        result = {}

        for matches in match_hash_list:
            # Get the id of the music, the offset in the database, and query the offset of the clip itself
            music_id_fk, offset_database, offset_query = matches

            # Calculate the difference between the offset of the music
            # in the database and the offset of the query segment itself
            offset = int(int(offset_database) - int(offset_query))

            # If offset does not exist in the dictionary, add it
            if offset not in result:
                result[offset] = {}

            if music_id_fk not in result[offset]:
                result[offset][music_id_fk] = 0

            # Count the number of occurrences of the song at the current offset
            result[offset][music_id_fk] += 1

            if result[offset][music_id_fk] > max_hash_count:
                # Update the value of max_hash_count
                max_hash_count = result[offset][music_id_fk]
                # assign song id
                music_id = music_id_fk
                # Assign the offset of the song
                music_offset = offset
                pass
            pass
            pass

        return {
            "music_id": music_id,
            "music_offset": music_offset,
            "max_hash_count": max_hash_count
        }

    # Calculate the fingerprint
    def _calculation_hash(self, music_path):
        """
            Calculate fingerprint
            :param music_path: path of music
            :return: fingerprint [(hash,t1), (hash,t1)...]
        """
        # Music preprocessing, converted to spectrogram (spectrum matrix)
        spectrogram = self._pre_music(music_path)

        # process spectrogram
        spectrogram = self._spectrogram_handle(spectrogram)

        # Get peakes through the spectrogram
        peakes = self._fingerprint(spectrogram)

        # Get Hash through peakes and return
        return self._generate_hash(peakes)

    # Music preprocessing, converted to spectrogram (spectrum matrix)
    def _pre_music(self, music_path):
        """
            Music preprocessing, converted to spectrogram (spectrum matrix)
            :param music_path: path of music
            :return: spectrogram
        """
        # load songs
        # y, sr = librosa.load(music_path, sr=16000)
        # print(sr)
        DATA1, SR1 = sf.read(music_path, channels=2, samplerate=48000, dtype=np.float32, subtype='PCM_32', format="RAW",
                             endian='LITTLE')
        y = DATA1.T
        y = librosa.resample(y, SR1, 16000)
        y = librosa.tone(220, length=256)
        print(y)
        # Do short-time Fourier transform
        arr_2d = librosa.stft(y,
                              n_fft=hp.fingerprint.core.stft.n_fft,
                              hop_length=hp.fingerprint.core.stft.hop_length,
                              win_length=hp.fingerprint.core.stft.win_length
                              )

        # What is returned is (frequency, time)
        return np.abs(arr_2d)

    pass

    # draw a graph of the linear relationship
    def _show_line_plot(self, match_hash):

        c = [item[0] for item in match_hash]

        x_and_y = [(item[1], item[2]) for item in match_hash]

        x = [int(item[0]) for item in x_and_y]
        y = [int(item[0]) for item in x_and_y]

        plt.scatter(x, y, c=c, marker='o')
        plt.show()

        pass
