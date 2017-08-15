from ....aipcloud.sound import Speech2Text
from urllib import (request as rqst, error)
from flask import abort, jsonify, g
import subprocess
import io
import os


def speech2text(url, speechClient):
    if url is None:
        abort(400, 'Make sure you have correctly entered the audio_url in the JSON format.')
    try:
        # get the audio format
        response = rqst.urlopen(url)
        mime = response.info()['Content-type']
        frmt = mime.split('/')[-1]
        # download the audio
        if mime.endswith("x-wav"):
            audio_name = 'audio.wav'
        elif mime.endswith("mpeg"):
            audio_name = 'audio.mp3'
        else:
            audio_name = 'audio.' + frmt
        args = ['wget', '-O', 'src/access_points/analyze/sound/' + audio_name, url]
        subprocess.check_call(args)
        # The name of the audio file to transcribe
        file_name = os.path.join(
            os.path.dirname(__file__),
            audio_name)

        # Loads the audio into memory
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
        analysis = speechClient.analyze(content)

        data = {
            'alternatives': analysis['res']
            }

        subprocess.call(['rm', '-f', audio_name])
        # g.user.save_query('/analyze/sound/speech2text', data, analysis['exec_time'])
        return jsonify(data)
    except error.HTTPError as err:
        return (jsonify({'Error in the image URL': 'Code Error: {}'.format(err.code)}), 400, {})
    except error.URLError as e:
        return (jsonify({'Error': 'There is an error in the image URL'}), 400, {})
    # except Exception as e:
        # abort(500, e)
