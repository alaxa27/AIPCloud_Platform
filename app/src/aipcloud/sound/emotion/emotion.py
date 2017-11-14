# -*- coding: utf-8 -*-
import os
from keras.models import model_from_json, Model
import time
import numpy as np
import soundfile as sf
import librosa
import configparser


class SpeechEmotionAnalyzer:
    def __init__(self):
        self.loaded = False
        self.model = None

    def refFun(self, S):
    	return np.log10(1 + 10000 * S)

    def load(self):
        if not self.loaded:
            # We load the JSON file and create the model
            json_file = open(os.path.join(os.sep, 'data/sound/emotion/model.json'), 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            self.model = model_from_json(loaded_model_json)
            # We load the weights into our model
            self.model.load_weights(
                os.path.join(os.sep, "data/sound/emotion/weights.h5"))
            self.loaded = True

            # Setting parameters

            cfg = configparser.ConfigParser()
            cfg.read(os.path.join(os.path.dirname(__file__), 'config.cfg'))

            self.FRAME_LENGTH = int(cfg.get("MEL", "frame_length"))
            self.NUMBER_MELS = int(cfg.get("MEL", "n_mels"))
            self.CLASSES = [ "neutral", "calm  ", "happy  ", "sad   ", "angry ", "fearful", "surpris", "disgust" ]

            dataset_shape = (self.FRAME_LENGTH / 10) * self.NUMBER_MELS
            self.X_test_vectors = [ np.repeat(0, dataset_shape) ]

            print("* Loaded model from disk")

    def analyze(self, inputFile):
        if not(self.loaded):
            raise UnloadedException()

        timeS = time.time()

        try:
            (signal, samplerate) = sf.read(inputFile)
        except:
            print(
                "Error with chunk file. Unable to perform features extraction on the file.")
            raise Exception()

        signal = librosa.to_mono(np.transpose(signal))
        trimmedSignal, _ = librosa.effects.trim(signal, top_db=50)
        spectrogram = librosa.feature.melspectrogram(trimmedSignal, sr=samplerate, n_fft=1024, hop_length=160)

        logSpectrogram = self.refFun(spectrogram)

        signalLength = float(len(trimmedSignal) / samplerate) * 1000
        indexPosition = 0
        while indexPosition < signalLength - self.FRAME_LENGTH:
        	row = np.asarray(logSpectrogram[:, int(indexPosition / 10):int((indexPosition + self.FRAME_LENGTH) / 10)]).ravel()
        	self.X_test_vectors.append(row)
        	indexPosition += self.FRAME_LENGTH

        self.X_test_vectors = self.X_test_vectors[1:]
        X_test = []
        for i in range(len(self.X_test_vectors)):
        	matrix = np.zeros((self.NUMBER_MELS, int(self.FRAME_LENGTH / 10)))
        	for l in range(self.NUMBER_MELS):
        		for m in range(int(self.FRAME_LENGTH / 10)):
        			matrix[l, m] = self.X_test_vectors[i][l * int(self.FRAME_LENGTH / 10) + m]
        	X_test.append([matrix])

        predict = self.model.predict(X_test)
        results = []
        for k in range(len(predict)):
            results.append({})
            for i in range(len(self.CLASSES)):
                results[k][self.CLASSES[i]] = float(round(predict[k][i], 4))

        return {'res': results, 'exec_time': time.time() - timeS}
