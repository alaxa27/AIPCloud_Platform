import time

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

class Speech2Text():
    def __init__(self):
        # Instantiates a client
        self.client = speech.SpeechClient()
        self.config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='fr-FR')



    def analyze(self, content):
        timeS = time.time()
        audio = types.RecognitionAudio(content=content)

        # Detects speech in the audio file
        response = self.client.recognize(self.config, audio)
        alternatives = response.results[0].alternatives

        results = []

        for alternative in alternatives:
            results.append(alternative.transcript)

        return {'res': results, 'exec_time': time.time() - timeS}
