import abc


class IConnector(abc.ABC):
    def __init__(self):
        pass

    # How to connect
    @abc.abstractmethod
    def _connection(self):
        raise NotImplementedError(u"Something went wrong, you did not implement the _connection abstract method")

    # store fingerprint
    @abc.abstractmethod
    def store_finger_prints(self, hashes, music_id_fk):
        raise NotImplementedError(
            u"Something went wrong, you did not implement the store_finger_prints abstract method")

    # Method to save a fingerprint
    @abc.abstractmethod
    def _add_finger_print(self, item, music_id_fk):
        raise NotImplementedError(u"Something went wrong, you did not implement the add_finger_print abstract method")

    # Find music according to the path of the music
    @abc.abstractmethod
    def find_music_by_music_path(self, music_path):
        raise NotImplementedError(
            u"Something went wrong, you did not implement the find_music_by_music_path abstract method")

    # Find out how many Hash numbers this song has according to the music id
    @abc.abstractmethod
    def calculation_hash_num_by_music_id(self, music_id):
        raise NotImplementedError(
            u"Something went wrong, you did not implement the calculation_hash_num_by_music_id abstract method")

    # add songs
    @abc.abstractmethod
    def add_music(self, music_path):
        raise NotImplementedError(u"Something went wrong, you did not implement the add_music abstract method")

    # Find a fingerprint
    @abc.abstractmethod
    def _find_finger_print(self, hash):
        raise NotImplementedError(u"Something went wrong, you did not implement the _find_finger_print abstract method")

    # Find fingerprints
    @abc.abstractmethod
    def find_math_hash(self, hashes):
        raise NotImplementedError(u"Something went wrong, you did not implement the find_math_hash abstract method")

    pass
