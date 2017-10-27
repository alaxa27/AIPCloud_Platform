from urllib import (request as rqst, error)
from flask import abort, jsonify, g
from werkzeug.utils import secure_filename
import subprocess
import io
import os

from ....aipcloud.sound import Speech2Text
from .... import app


def speech2text(file, speechClient):
    if file is None:
        abort(400, 'Please make sure you have correctly entered the audio_url in the JSON format.')

    try:
        UPLOAD_FOLDER = './uploads'
        ALLOWED_EXTENSIONS = set(['wav', 'mp3', 'flac'])

        if allowed_file(ALLOWED_EXTENSIONS, file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(os.path.dirname(
                __file__), UPLOAD_FOLDER, filename)
            file.save(file_path)
        else:
            raise Exception("The file's format you provided is not accepted.")

        # subprocess.call(['sox', file_path, file_path + '.flac'])

        subprocess.call(['sox', file_path, '-t', 'raw', '--channels=1', '--bits=16', '--rate=16000', '--encoding=signed-integer', '--endian=little', file_path + '.raw'])

        raw_file = file_path + '.raw'
        # Loads the audio into memory
        with io.open(raw_file, 'rb') as audio_file:
            content = audio_file.read()
        analysis = speechClient.analyze(content)
        
        data = {
            'results': analysis['res']
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
        try:
            subprocess.call(['rm', '-f', file_path + '*'])
        except Exception as e:
            abort(500, e)

def allowed_file(ALLOWED_EXTENSIONS, filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
