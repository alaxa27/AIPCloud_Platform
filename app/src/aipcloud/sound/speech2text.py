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

        if len(response.results) == 0:
            raise Exception('The server did not send any recognition results.')
        alternatives = response.results[0].alternatives

        results = []

        for res in response:
            results.append({
                'transcript': res.alternative[0].transcript,
                'confidence': str(res.alternative[0].confidence)
            })

        return {'res': results, 'exec_time': time.time() - timeS}
