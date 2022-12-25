from core.ICore.IMusicProcessor import IMusicProcessor
import abc


class IMusicProcessorPredict(IMusicProcessor):

    @abc.abstractmethod
    def predict_music(self, music_path, connector):
        raise NotImplementedError(u"Something went wrong, you did not implement the predict_music abstract method")


    pass