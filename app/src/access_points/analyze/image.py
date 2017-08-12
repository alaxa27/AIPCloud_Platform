from ...aipcloud.image import classifier, utils
from urllib import (request as rqst, error)
from flask import abort, jsonify, g
import subprocess

def classify(url):
    if url is None:
        abort(400, 'Make sure you correctly entered image_url in the json format.')
    try:
        # get the image format
        response = rqst.urlopen(url)
        mime = response.info()['Content-type']
        frmt = mime.split('/')[-1]
        # download the image
        if mime.endswith("jpeg"):
            image_name = 'database/image.jpg'
        else:
            image_name = 'database/image.' + frmt
        args = ['wget', '-O', image_name, url]
        subprocess.check_call(args)
        # Call the image analysis model
        imgClassifier = classifier.MultiLabelClassifier()
        imgClassifier.load()
        results = imgClassifier.classify( image_name, nbClasses=1000)
        data = {}
        for r in results:
        	if r[1] > 0.005:
                    data[r[0]] = round((r[1] * 100),2)
        # Delete the image after getting the analysis results
        subprocess.call(['rm', '-f', image_name])
        g.user.save_query('/analyze/image', data, 1)
        return jsonify(data)
    except error.HTTPError as err:
        return (jsonify({'Error in the image URL': 'Code Error: {}'.format(err.code)}), 400, {})
    except error.URLError as e:
        return (jsonify({'Error': 'There is an error in the image URL'}), 400, {})
    except Exception as e:
        abort(500, e)
