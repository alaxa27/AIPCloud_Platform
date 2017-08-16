from ....aipcloud.sound import Speech2Text
from urllib import (request as rqst, error)
from flask import abort, jsonify, g
import subprocess
import io, os


def speech2text(url, speechClient):
    if url is None:
        abort(400, 'Please make sure you have correctly entered the audio_url in the JSON format.')
    try:
        # get the audio format
        response = rqst.urlopen(url)
        mime = response.info()['Content-type']
        frmt = mime.split('/')[-1]
        # download the audio
        if mime.endswith("x-wav"):
            audio_name = 'database/audio.wav'
        elif mime.endswith("mpeg"):
            audio_name = 'database/audio.mp3'
            raise Exception('Filetype not supported.')
        else:
            audio_name = 'database/audio.' + frmt
        args = ['wget', '-O', audio_name, url]
        subprocess.check_call(args)
        subprocess.call(['sox', audio_name, '-t', 'raw', '--channels=1', '--bits=16', '--rate=16000', '--encoding=signed-integer', '--endian=little', 'database/audio.raw'])
        # The name of the audio file to transcribe
        file_name = os.path.join(
            os.path.dirname(__file__),
            '../../../../' + 'database/audio.raw')
        # Loads the audio into memory
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
        analysis = speechClient.analyze(content)
        data = {
            'alternatives': analysis['res']
            }
        # Save the query into the database
        g.user.save_query('/analyze/sound/speech2text', data, analysis['exec_time'])
        return jsonify(data)
    except error.HTTPError as err:
        return (jsonify({'Error in the image URL': 'Code Error: {}'.format(err.code)}), 400, {})
    except error.URLError as e:
        return (jsonify({'Error': 'There is an error in the image URL'}), 400, {})
    except Exception as e:
        abort(500, e)
    finally:
        # Delete the audio under all circumstances
        subprocess.call(['rm', '-f', audio_name])
        subprocess.call(['rm', '-f', 'database/audio.raw'])
