# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import librosa
import configparser
import soundfile as sf
from keras.models import model_from_json
from keras import backend as K
from sklearn.cluster import AgglomerativeClustering, KMeans, DBSCAN
import sklearn
import tensorflow as tf
from scipy.cluster.hierarchy import dendrogram, linkage


class SpeakerClusterAnalyzer:
    def __init__(self):
        self.loaded = False
        self.model = None

    def refFun(S):
    	return np.log10(1 + 10000 * S)

    def load(self):
        if not self.loaded:
            # We load the JSON file and create the model
            json_file = open(os.path.join(os.path.dirname(__file__), '../../data/sound/cluster/model.json'), 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            self.model = model_from_json(loaded_model_json)
            # We load the weights into our model
            self.model.load_weights(
                os.path.join(os.path.dirname(__file__), "../../data/sound/cluster/weights.h5"))
            self.loaded = True
            print("* Loaded model from disk")

    def analyze(self, inputFile, count=2):
        if not(self.loaded):
            raise UnloadedException()

        timeS = time.time()
        cfg = configparser.ConfigParser()
        cfg.read(os.path.join(os.path.dirname(__file__), 'config.cfg'))

        SOUND_FORMAT = cfg.get("IO", "sound_format")
        PARAM_FRAME_LENGTH = int(cfg.get("MEL", "frame_length"))
        PARAM_NUMBER_MELS = int(cfg.get("MEL", "n_mels"))

        K.set_learning_phase(False)

        # The number of columns in the dataset (except for index)
        dataset_shape = (PARAM_FRAME_LENGTH / 10) * PARAM_NUMBER_MELS
        X_test_vectors = [ np.repeat(0, dataset_shape) ]


        try:
            (signal, samplerate) = sf.read(inputFile)
        except:
            print(
                "Error with chunk file. Unable to perform features extraction on the file.")
            raise Exception()

        signal, _ = librosa.effects.trim(signal, top_db=50)
        #spectrogram = librosa.feature.melspectrogram(signal, sr=samplerate, n_fft=1024, hop_length=160, fmin=240, fmax=3000)
        spectrogram = librosa.feature.melspectrogram(signal, sr=samplerate, n_fft=1024, hop_length=160)


        logSpectrogram = self.refFun(spectrogram)

        signalLength = float(len(signal) / samplerate) * 1000
        indexPosition = 0
        while indexPosition < signalLength - PARAM_FRAME_LENGTH:
        	row = np.asarray(logSpectrogram[:, int(indexPosition / 10):int((indexPosition + PARAM_FRAME_LENGTH) / 10)]).ravel()
        	X_test_vectors.append(row)
        	indexPosition += PARAM_FRAME_LENGTH
        X_test_vectors = X_test_vectors[1:] # We remove first row which is only 0

        X_test = []
        for i in range(len(X_test_vectors)):
        	matrix = np.zeros((PARAM_NUMBER_MELS, int(PARAM_FRAME_LENGTH / 10)))
        	for l in range(PARAM_NUMBER_MELS):
        		for m in range(int(PARAM_FRAME_LENGTH / 10)):
        			matrix[l, m] = X_test_vectors[i][l * int(PARAM_FRAME_LENGTH / 10) + m]
        	X_test.append([matrix])

        # Creating vector into clustering space
        cluster_space_layer = K.function([self.model.layers[0].input], [self.model.layers[7].output])
        layer_output = cluster_space_layer([X_test])[0]

        cosinus_dist = 1. - sklearn.metrics.pairwise.cosine_similarity(layer_output)
        cosinus_dist[cosinus_dist < 0] = 0
        cosine_tsne = manifold.TSNE(n_components=2, metric='precomputed').fit_transform(cosinus_dist)

        Z = linkage(layer_output, metric='cosine', method='complete')
        dendrogram(
        	Z,
        	show_leaf_counts=False,  # otherwise numbers in brackets are counts
        	leaf_rotation=90.,
        	leaf_font_size=12.)

        minDist = max([row[2] for row in Z])
        nb_clusters = len(Z)
        for i in range(len(Z)-1):
        	if (minDist > Z[i+1][2] - Z[i][2]):
        		minDist = Z[i+1][2] - Z[i][2]
        		nb_clusters = i

        if count is None:
            count = 2
        int(count)
        clustering = AgglomerativeClustering(affinity='cosine', linkage="complete", n_clusters=count).fit_predict(layer_output)
        clustering_list = list(clustering)
        #clustering = KMeans(n_clusters=4).fit_predict(layer_output)
        return {'res': clustering_list, 'exec_time': time.time() - timeS}
