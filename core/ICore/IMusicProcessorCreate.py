import abc
from core.ICore.IMusicProcessor import IMusicProcessor


class IMusicProcessorCreate(IMusicProcessor):

    # Interface for creating fingerprints and saving them to the database
    @abc.abstractmethod
    def create_finger_prints_and_save_database(self, music_path, connector):
        raise NotImplementedError(
            u"Something went wrong, you did not implement the create_finger_prints_and_save_database abstract method")

    # process fingerprint
    @abc.abstractmethod
    def _calculation_hash(self, music_path):
        raise NotImplementedError(u"Something went wrong, you did not implement the _calculation_hash abstract method")

    # Music preprocessing, converted to spectrogram (spectrum matrix)
    @abc.abstractmethod
    def _pre_music(self, music_path):
        raise NotImplementedError(u"Something went wrong, you did not implement the _pre_music abstract method")

    pass
