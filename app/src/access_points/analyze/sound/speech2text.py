from ....aipcloud.sound import Speech2Text

def speech2text(url, speechClient):
    if url is None:
        abort(400, 'Make sure you correctly entered audio_url in the json format.')
    try:
        # get the image format
        response = rqst.urlopen(url)
        mime = response.info()['Content-type']
        frmt = mime.split('/')[-1]
        # download the image
        if mime.endswith("wav"):
            audio_name = 'database/audio.wav'
        else:
            audio_name = 'database/audio.' + frmt
        args = ['wget', '-O', audio_name, url]
        subprocess.check_call(args)
        # Call the image analysis model

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

        subprocess.call(['rm', '-f', image_name])
        g.user.save_query('/analyze/image', data, analysis['exec_time'])
        return jsonify(data)
    except error.HTTPError as err:
        return (jsonify({'Error in the image URL': 'Code Error: {}'.format(err.code)}), 400, {})
    except error.URLError as e:
        return (jsonify({'Error': 'There is an error in the image URL'}), 400, {})
    except Exception as e:
        abort(500, e)
