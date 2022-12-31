import os
import soundfile
import io
import glob
import ffmpeg
from typing import Literal
from urllib import request
# import librosa
# from tqdm import tqdm
# import numpy as np
# import soundfile as sf 
from flask import Flask, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

from predict import predict

app = Flask(__name__)
CORS(app)

@app.post('/find_song')
def find_song():
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join("./datatest1", filename)
    file.save(filepath)
    stream = ffmpeg.input(filepath)
    stream = ffmpeg.output(stream, "./datatest1/exported.wav")
    ffmpeg.run(stream)
    id = predict()
    os.remove("./datatest1/exported.wav")
    os.remove(filepath)

    return id

if __name__ == "__main__":
    app.run()