from urllib import (request as rqst, error)
from flask import abort, jsonify, g
from werkzeug.utils import secure_filename
import subprocess
import io, os

from .... import app

def recognition(file, speechEmotionAnalyzer):
    if file is None:
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
        # The name of the audio file to transcribe
        UPLOAD_FOLDER = './uploads'
        ALLOWED_EXTENSIONS = set(['wav', 'mp3'])

        if allowed_file(ALLOWED_EXTENSIONS, file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(os.path.dirname(__file__), UPLOAD_FOLDER, filename)
            file.save(file_path)
        else:
            raise Exception("The file's format you provided is not accepted.")

        subprocess.call(['sox', file_path, file_path + '.wav'])
        # Loads the audio into memory
        analysis = speechEmotionAnalyzer.analyze(file_path + '.wav')
        results = analysis['res']
        data = {
            'neutral': float(round(results[0], 4)),
            'happy': float(round(results[1], 4)),
            'calm': float(round(results[2], 4)),
            'sad': float(round(results[3], 4)),
            'angry': float(round(results[4], 4)),
            'fearful': float(round(results[5], 4)),
            'disgust': float(round(results[6], 4)),
            'surprise': float(round(results[7], 4))
            }
        # Save the query into the database
        g.user.save_query('/analyze/sound/emotion', data, analysis['exec_time'])
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
