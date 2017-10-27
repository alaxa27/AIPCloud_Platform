import time

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import storage


class Speech2Text():
    def __init__(self):
        self.storageClient = storage.Client()
        # Get bucket:
        try:
            self.bucket = self.storageClient.get_bucket('aipcloud-bucket')
        except google.cloud.exceptions.NotFound:
            raise Exception('Sorry, that bucket does not exist!')
        # Instantiates a client
        self.client = speech.SpeechClient()
        self.config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='fr-FR')

    def analyze(self, fileName, filePath):
        timeS = time.time()

        # UPLOAD THE FILE TO GCS
        blob = self.bucket.blob(fileName)
        blob.upload_from_filename(filePath)
        # Make sure the file has a unique name
        # Then feed the analyzer with the URI provided by GCS
        uri = blob.self_link
        audio = types.RecognitionAudio(uri=uri)

        # Detects speech in the audio file
        response = self.client.long_running_recognize(self.config, audio)
        #Delete file from GCS
        blob.delete()

        if len(response.results) == 0:
            raise Exception('The server did not send any recognition results.')
        alternatives = response.results[0].alternatives

        results = []

        for res in response.results:
            results.append({
                'transcript': res.alternatives[0].transcript,
                'confidence': str(res.alternatives[0].confidence)
            })

        return {'res': results, 'exec_time': time.time() - timeS}
