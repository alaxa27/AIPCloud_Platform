from urllib import (request as rqst, error)
from flask import abort, jsonify, g
from werkzeug.utils import secure_filename
import subprocess
import io, os

from ....aipcloud.sound import Speech2Text


def speech2text(file, speechClient):
    if url is None:
        abort(400, 'Please make sure you have correctly entered the audio_url in the JSON format.')
    try:
        # get the audio format
        # response = rqst.urlopen(url)
        # mime = response.info()['Content-type']
        # frmt = mime.split('/')[-1]
        # # download the audio
        # if mime.endswith("x-wav"):
        #     audio_name = 'database/audio.wav'
        # elif mime.endswith("mpeg"):
        #     audio_name = 'database/audio.mp3'
        #     raise Exception('Filetype not supported.')
        # else:
        #     audio_name = 'database/audio.' + frmt
        # args = ['wget', '-O', audio_name, url]
        # subprocess.check_call(args)
        # subprocess.call(['sox', audio_name, '-t', 'raw', '--channels=1', '--bits=16', '--rate=16000', '--encoding=signed-integer', '--endian=little', 'database/audio.raw'])
        # The name of the audio file to transcribe
        UPLOAD_FOLDER = '../../../../database'
        ALLOWED_EXTENSIONS = set(['wav'])
        if allowed_file(ALLOWED_EXTENSIONS, file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            raise Exception("The format of the file you provided is not accepted.")

        subprocess.call(['sox', filename, '-t', 'raw', '--channels=1', '--bits=16', '--rate=16000', '--encoding=signed-integer', '--endian=little', filename + '.raw'])
        file_name = os.path.join(
            os.path.dirname(__file__),
            '../../../../' + 'database/audio.raw')
        raw_file = os.path.join(UPLOAD_FOLDER, filename) + '.raw'
        # Loads the audio into memory
        with io.open(raw_file, 'rb') as audio_file:
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

def allowed_file(ALLOWED_EXTENSIONS, filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
