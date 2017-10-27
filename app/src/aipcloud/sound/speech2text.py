import time
from uuid import uuid4

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import storage


class Speech2Text():
    def __init__(self):
        self.storageClient = storage.Client()
        self.bucket_name = 'aipcloud-bucket'
        # Get bucket:
        try:
            self.bucket = self.storageClient.get_bucket(self.bucket_name)
        except google.cloud.exceptions.NotFound:
            raise Exception('Sorry, that bucket does not exist!')
        # Instantiates a client
        self.client = speech.SpeechClient()
        self.config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='fr-FR')

    def analyze(self, filePath):
        timeS = time.time()

        # UPLOAD THE FILE TO GCS
        fileName = str(uuid4()) + '.raw'
        blob = self.bucket.blob(fileName)
        blob.upload_from_filename(filePath)
        # Make sure the file has a unique name
        # Then feed the analyzer with the URI provided by GCS
        uri = 'gs://' + self.bucket_name + '/' + fileName#blob.self_link

        audio = types.RecognitionAudio(uri=uri)

        try:
            # Detects speech in the audio file
            operation = self.client.long_running_recognize(config=self.config, audio=audio)

            retry_count = 50
            while retry_count > 0 and not operation.done():
                retry_count -= 1
                time.sleep(1)

            operationResults = operation.result().results
            if len(operationResults) == 0:
                raise Exception('The server did not send any recognition results.')

            results = []
            for res in operationResults:
                results.append({
                    'transcript': res.alternatives[0].transcript,
                    'confidence': str(res.alternatives[0].confidence)
                })

            blob.delete()
            return {'res': results, 'exec_time': time.time() - timeS}
        except:
            #Delete file from GCS
            blob.delete()
