#!/usr/bin/env python
# -*- coding: utf-8 -*
from src.models import User
from src import app, db, auth
from src.authentication import Authentication
from src.initialize_db import InitializeDB
from src.snippets.snippets import dialA, dialB
from flask import abort, request, jsonify, g, url_for
from flask_cors import CORS, cross_origin
from src.aipcloud.text import sentiment
from src.aipcloud.image import classifier, utils
import cv2
import numpy as np
import logging
from time import time
import subprocess
from urllib import (request as rqst, error)

app = CORS(app)


@auth.verify_password
def verify_password(email_or_token, password):
    authenticate = Authentication()
    return authenticate.verify_password(email_or_token, password)


@app.route('/init')
def initialization():
    try:
        print("-------------------------->>No database.")
        InitializeDB(db)
        import nltk
        nltk.download("punkt")
        return "200"
    except:
        if not os.path.exists('database/db.sqlite'):
            return "400"


@app.route('/token')
@auth.login_required
def get_auth_token():
    auths = g.user.points
    counter = 0
    l = []
    for element in auths:
        if element.timeref >= int(time()) - 86400:
            l.append(element.timeref)
            counter = 1
    if counter == 0:
        abort(403)
    timeref = max(l)
    expiration = timeref + 86400 - int(time())
    if expiration <= 0:
        abort(403)
    m, s = divmod(expiration, 60)
    h, m = divmod(m, 60)
    token = g.user.generate_auth_token(expiration)
    return jsonify({'token': token.decode('ascii'), 'expires-in': "%dh %02dmin %02ds" % (h, m, s)})


@app.route('/analyze/sentence', methods=['POST'])
@auth.login_required
def analyze_sentence():
    user = g.user
    user.verify_access('/analyze/sentence')
    sentence = request.json.get('sentence')
    if sentence is None:
        abort(400)
    sentenceAnalyzer = sentiment.SentenceSentimentAnalyzer()
    sentenceAnalyzer.load()
    results = sentenceAnalyzer.analyze(sentence)
    return jsonify({'Positif': round(results[2] * 100, 2),
                    'Neutre': round(results[1] * 100, 2),
                    'Negatif': round(results[0] * 100, 2)  })


@app.route('/analyze/text', methods=['POST'])
@auth.login_required
def analyze_text():
    user = g.user
    user.verify_access('/analyze/text')
    text = request.json.get('text')
    if text is None:
        abort(400)
    textAnalyzer = sentiment.TextSentimentAnalyzer()
    textAnalyzer.load()
    results = textAnalyzer.analyze(text, verbose=False)
    return jsonify({'Positif': round(results[2] * 100, 2),
                    'Neutre': round(results[1] * 100, 2),
                    'Negatif': round(results[0] * 100, 2),
                    'Pertinence': round(results[3] * 100, 2)})


@app.route('/analyze/customer', methods=['POST'])
@auth.login_required
def customer_service_analyzer():
    user = g.user
    user.verify_access('/analyze/customer')
    sentence = request.json.get('sentence')
    if sentence is None:
        abort(400)
    textCS = sentiment.CustomerServiceAnalyzer()
    textCS.load()
    results = textCS.analyze(sentence)
    return jsonify({'Sentiment': round(results[0] * 100, 2),
                    'Agressivite': round(results[1] * 100, 2),
                    'Remboursement': round(results[2] * 100, 2) })


@app.route('/analyze/dialogue', methods=['GET'])
@auth.login_required
def dialogue_analyzer():
    user = g.user
    user.verify_access('/analyze/dialogue')
    dialogueAnalyzer = sentiment.DialogueSentimentAnalyzer()
    dialogueAnalyzer.load()
    resultsA, resultsB, estim = dialogueAnalyzer.analyze(dialB, dialA, verbose=False)
    return jsonify({"Positif A": round(resultsA[2] * 100, 2),
                    "Neutre A": round(resultsA[1] * 100, 2),
                    "Negatif A": round(resultsA[0] * 100, 2),
                    "Pertinence A": round(estim[0] * 100, 2),
                    "Pente A": round(estim[3], 4),
                    "Positif B": round(resultsB[2] * 100, 2),
                    "Neutre B": round(resultsB[1] * 100, 2),
                    "Negatif B": round(resultsB[0] * 100, 2),
                    "Pertinence B": round(estim[1] * 100, 2),
                    "Pente B": round(estim[4], 4),
                    "Pertinence totale": round(estim[2] * 100, 2)})


@app.route('/image', methods=['POST'])
@auth.login_required
def image_analyzer():
    user = g.user
    user.verify_access('/image')
    url = request.json.get('image-url')
    if url is None:
        abort(400)
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
        return jsonify(data)
    except error.HTTPError as err:
        return (jsonify({'Error in the image URL': 'Code Error: {}'.format(err.code)}), 400, {})
    except error.URLError as e:
        return (jsonify({'Error': 'There is an error in the image URL'}), 400, {})


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    import nltk
    nltk.download("punkt")
    # print("Checking if databse exists.")
    # if not os.path.exists('database/db.sqlite'):
    #     print("-------------------------->>No database.")
    #     InitializeDB(db)
    # This is used when running locally.
    app.run(host='0.0.0.0', debug=True)
