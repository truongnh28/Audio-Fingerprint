from utils.print_utils import print_error, print_message, print_warning
import numpy as np
import librosa
from utils.hparam import hp
from core.ICore.IMusicProcessorCreate import IMusicProcessorCreate


class STFTMusicProcessorCreate(IMusicProcessorCreate):

    # Create a fingerprint and save it to the database
    def create_finger_prints_and_save_database(self, music_path, connector):
        # Create a fingerprint and save it to the database
        # :param music_path: music path
        # :param connector: connect to the database
        # :return: None
        # First query to see if there is this song in the database
        music_id = connector.find_music_by_music_path(music_path=music_path)

        # If there is no such song in the database
        if music_id is None:
            # Add a song and get the song id
            music_id = connector.add_music(music_path)

            # Calculate Hash
            # hashes = list(self._calculation_hash(music_path=music_path))

            # Save the Hash value to the database
            # connector.store_finger_prints(hashes=hashes, music_id_fk=music_id)

            # Hash number of songs
            # hash_num = connector.calculation_hash_num_by_music_id(music_id=music_id)
            # print prompt information
            # print_message("song: " + str(music_id) + " Added successfully! \nHash number is:" + str(hash_num) + "\n")
            pass
        # If the song exists in the database
        else:
            # Calculate the number of Hash of this song
            hash_num = connector.calculation_hash_num_by_music_id(music_id=music_id)
            print_warning(
                "the song " + str(music_id) + " already exists, there are" + str(hash_num) + "Article Hash!!!")
            pass

        pass

    # Calculate the fingerprint
    def _calculation_hash(self, music_path):
        # Calculate fingerprint
        # :param music_path: path of music
        # :return: fingerprint [(hash,t1), (hash,t1)...]
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
        y, sr = librosa.load(music_path, sr=hp.fingerprint.core.stft.sr)

        # Do short-time Fourier transform
        arr_2d = librosa.stft(y,
                              n_fft=hp.fingerprint.core.stft.n_fft,
                              hop_length=hp.fingerprint.core.stft.hop_length,
                              win_length=hp.fingerprint.core.stft.win_length)

        # What is returned is (frequency, time)
        print(np.abs(arr_2d))
        return np.abs(arr_2d)
