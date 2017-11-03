# -*- coding: utf-8 -*-
import os
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.convolutional import Convolution1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.models import model_from_json
import numpy as np
import time
import math
import pandas as pd
import configparser
from .MFCC import mfcc
import scipy.io.wavfile as wav
import soundfile as sf

try:
    import matplotlib.pyplot as plt
except:
    print("Matplotlib not installed.")


def pad_sequence_into_array(Xs, maxlen=None, truncating='post', padding='post', value=0.):
    """
    Padding sequence (list of numpy arrays) into an numpy array
    :param Xs: list of numpy arrays. The arrays must have the same shape except the first dimension.
    :param maxlen: the allowed maximum of the first dimension of Xs's arrays. Any array longer than maxlen is truncated to maxlen
    :param truncating: = 'pre'/'post', indicating whether the truncation happens at either the beginning or the end of the array (default)
    :param padding: = 'pre'/'post',indicating whether the padding happens at either the beginning or the end of the array (default)
    :param value: scalar, the padding value, default = 0.0
    :return: Xout, the padded sequence (now an augmented array with shape (Narrays, N1stdim, N2nddim, ...)
    :return: mask, the corresponding mask, binary array, with shape (Narray, N1stdim)
    """
    Nsamples = len(Xs)
    if maxlen is None:
        # 'sequences' must be list, 's' must be numpy array, len(s) return the first dimension of s
        lengths = [s.shape[0] for s in Xs]
        maxlen = np.max(lengths)

    Xout = np.ones(shape=[Nsamples, maxlen] + list(Xs[0].shape[1:]),
                   dtype=Xs[0].dtype) * np.asarray(value, dtype=Xs[0].dtype)
    Mask = np.zeros(shape=[Nsamples, maxlen], dtype=Xout.dtype)
    for i in range(Nsamples):
        x = Xs[i]
        if truncating == 'pre':
            trunc = x[-maxlen:]
        elif truncating == 'post':
            trunc = x[:maxlen]
        else:
            raise ValueError(
                "Truncating type '%s' not understood" % truncating)
        if padding == 'post':
            Xout[i, :len(trunc)] = trunc
            Mask[i, :len(trunc)] = 1
        elif padding == 'pre':
            Xout[i, -len(trunc):] = trunc
            Mask[i, -len(trunc):] = 1
        else:
            raise ValueError("Padding type '%s' not understood" % padding)
    return Xout, Mask


class SpeechEmotionAnalyzer:
    def __init__(self):
        self.loaded = False
        self.model = None

    def load(self):
        if not self.loaded:
            # We load the JSON file and create the model
            json_file = open(os.path.join(os.path.dirname(__file__), '../../data/sound/emotion/one_label.json'), 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            self.model = model_from_json(loaded_model_json)
            # We load the weights into our model
            self.model.load_weights(
                os.path.join(os.path.dirname(__file__), "../../data/sound/emotion/one_label_weights.h5"))
            self.loaded = True
            print("* Loaded model from disk")

    def analyze(self, inputFile):
        if not(self.loaded):
            raise UnloadedException()

        timeS = time.time()
        BATCH_SIZE = 64
        EPOCHS = 14
        CLASSES = ["neutral", "calm  ", "happy  ", "sad   ",
                   "angry ", "fearful", "disgust", "surprise"]

        cfg = configparser.ConfigParser()
        cfg.read(os.path.join(os.path.dirname(__file__), 'config.cfg'))

        SOUND_FORMAT = cfg.get("IO", "sound_format")
        MFCC_FRAME = int(cfg.get("MFCC", "frame")) / 1000
        MFCC_OVERLAP = int(cfg.get("MFCC", "overlap")) / 1000
        MFCC_SAMPLERATE = int(cfg.get("MFCC", "samplerate"))
        MFCC_FBANK_CHANNELS = int(cfg.get("MFCC", "filterbank_channels"))
        MFCC_MAX_FRAMES = int(cfg.get("MFCC", "max_frames"))
        MFCC_CEPSTRUMS = int(cfg.get("MFCC", "cepstrums"))

        NUM_CLASSES = 8
        NUM_FEATURES = MFCC_CEPSTRUMS

        print("* Loading dataset")
        #dataset = pd.read_csv("data/train.csv").values[1:,1:]

        # We split the dataset into a train set and a test set
        #dataset_train = dataset[:TEST_TRAIN_LENGTH,:]
        #dataset_test = dataset[(len(dataset) - TEST_SET_LENGTH):,:]

        #X = dataset[:, 1:] * 100
        #tempX = []
        # for i in range(len(X)):
        #	row = X[i, :]
        #	newAdd = row.reshape(MFCC_MAX_FRAMES, MFCC_CEPSTRUMS)[np.newaxis, :][0]
        #	tempX.append(newAdd)
        #X = np.asarray(tempX)
        #X, _ = pad_sequence_into_array(X, maxlen=35)
        #test = X[6:7]

        try:
            (signal, _) = sf.read(inputFile)
        except:
            print(
                "Error with chunk file. Unable to perform features extraction on the file.")
            raise Exception()

        max_features_size = MFCC_MAX_FRAMES * MFCC_CEPSTRUMS
        data = np.array(np.repeat(0, max_features_size))
        feature = mfcc(signal, samplerate=MFCC_SAMPLERATE, winlen=MFCC_FRAME,
                       winstep=MFCC_OVERLAP, nfilt=MFCC_FBANK_CHANNELS, numcep=MFCC_CEPSTRUMS)
        print("Array of size " + str(len(feature)) +
              " x " + str(len(feature[0])))

        feature1D = feature.ravel()
        if len(feature1D) >= max_features_size:
            dataRow = np.hstack([feature1D[:max_features_size]])
        else:
            dataRow = np.hstack([feature1D, np.array(
                np.repeat(0, max_features_size - len(feature1D)))])

        data = np.array(dataRow)
        print(data)
        data = data.reshape(MFCC_MAX_FRAMES, MFCC_CEPSTRUMS)[np.newaxis, :][0]

        X, _ = pad_sequence_into_array([data], maxlen=80)
        predict = self.model.predict(X)

        print(predict[0])
        for i in range(8):
            print(" * " + CLASSES[i] + "\t" +
                  "{:1.2f} %".format(predict[0][i] * 100))

        return {'res': predict[0], 'exec_time': time.time() - timeS}
