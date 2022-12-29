import hashlib
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion, iterate_structure
from utils.hparam import hp
from utils.print_utils import print_error, print_message, print_warning
import numpy as np
import abc
import matplotlib.pyplot as plt



# Processing of music
class IMusicProcessor():

    # Interface for creating fingerprints and saving them to the database
    @abc.abstractmethod
    def create_finger_prints_and_save_database(self, music_path, connector):
        raise NotImplementedError(u"Something went wrong, you did not implement the create_finger_prints_and_save_database abstract method")

    # Calculate Hash
    @abc.abstractmethod
    def _calculation_hash(self, music_path):
        raise NotImplementedError(u"Something went wrong, you did not implement the _calculation_hash abstract method")

    # Music preprocessing, converted to spectrogram (spectrum matrix)
    @abc.abstractmethod
    def _pre_music(self, music_path):
        raise NotImplementedError(u"Something went wrong, you did not implement the _pre_music abstract method")

    # process spectrogram
    def _spectrogram_handle(self, spectrogram):
        # Working with spectrograms
        # :param spectrogram: spectrogram
        # :return: spectrogram after processing
        # replace the 0's of the spectrum matrix with the minimum
        min_ = np.min(spectrogram[np.nonzero(spectrogram)])

        # Replace all 0's with the minimum value obtained
        spectrogram[spectrogram == 0] = min_

        # get log
        spectrogram = 10 * np.log10(spectrogram)

        # Prevent data from being negative infinity
        spectrogram[spectrogram == -np.inf] = 0

        # Return the processed spectrogram
        return spectrogram

    # Get peakes through the spectrogram
    def _fingerprint(self, spectrogram):
        # Get peakes through spectrogram
        # :param spectrogram: spectrogram
        # :return: local maximum point
        # maximum_filter
        # Make the cross
        struct = generate_binary_structure(2, 1)
        # expand the cross
        neighborhood = iterate_structure(struct, hp.fingerprint.core.neighborhood)
        # Get the local maximum point
        local_max = maximum_filter(spectrogram, footprint=neighborhood) == spectrogram
        # Get the energy value of the local maximum
        amps = spectrogram[local_max]
        # leveling
        amps = amps.flatten()
        # Get the values of the time and frequency axes of the local maximum point,
        # j represents the frequency, and i represents the time
        j, i = np.where(local_max)
        # Get (time, frequency, energy value) triplet data is the peakes we want
        peakes = list(zip(i, j, amps))
        # Filter values with small energy
        peakes = [item for item in peakes if item[2] > hp.fingerprint.core.amp_min]
        # Drawing function, constellation diagram
        if hp.fingerprint.show_plot.create_database.planisphere_plot:
            self._draw_planisphere_plot(peakes)
            pass
        # time
        time_idx = [item[0] for item in peakes]
        # frequency
        freq_idx = [item[1] for item in peakes]
        # Wrap it up
        peakes = list(zip(time_idx, freq_idx))

        return peakes

    # Get Hash through peakes and return
    def _generate_hash(self, peakes):
        # Get Hash through peakes and return
        # :param peakes: peaks, local maximum point
        # :return: Hash，[(hash,t1), (hash, t1), ]
        # Sort by time
        peakes = sorted(peakes)

        # Traversing anchors
        for i in range(len(peakes)):
            # Loop through neighbors
            for j in range(1, hp.fingerprint.core.near_num):
                # Prevent subscripts from going out of bounds
                if i + j < len(peakes):
                    # time between two points
                    t1 = peakes[i][0]
                    t2 = peakes[i + j][0]

                    # Frequency of two points
                    f1 = peakes[i][1]
                    f2 = peakes[i + j][1]

                    # calculate time interval
                    t_delta = t2 - t1
                    if hp.fingerprint.core.min_time_delta <= t_delta <= hp.fingerprint.core.max_time_delta:
                        # Calculate Hash
                        hash_str = "%s|%s|%s" % (f1, f2, t_delta)
                        # Generate Hash
                        hash_str = hashlib.sha1(hash_str.encode("utf-8"))
                        yield hash_str.hexdigest(), t1

                    pass
                pass
            pass

        pass

    # Draw the constellation diagram
    def _draw_planisphere_plot(self, peakes):

        x_and_y = [(item[1], item[0]) for item in peakes]

        # x-coordinate
        x = [int(item[0]) for item in x_and_y]
        # y-coordinate
        y = [int(item[1]) for item in x_and_y]

        # plt.scatter(x, y, marker='x')
        # plt.show()


        pass

    pass
