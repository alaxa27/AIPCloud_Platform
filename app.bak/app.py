#!/usr/bin/env python
# -*- coding: utf-8 -*
from src.models import User
from src import app, db, auth
from src.authentication import Authentication
from src.initialize_db import InitializeDB
import os
from flask import abort, request, jsonify, g, url_for
from src.aipcloud.text import sentiment
from src.aipcloud.image import classifier, utils
import cv2
import numpy as np
import logging
from time import time
import subprocess
import urllib2


@auth.verify_password
def verify_password(email_or_token, password):
    authenticate = Authentication()
    return authenticate.verify_password(email_or_token, password)


@app.route('/token')
@auth.login_required
def get_auth_token():
    timeref = g.user.timeref
    expiration = timeref + 86400 - int(time())
    m, s = divmod(expiration, 60)
    h, m = divmod(m, 60)
    token = g.user.generate_auth_token(expiration)
    return jsonify({'token': token.decode('ascii'), 'expires-in': "%dh %02dmin %02ds" % (h, m, s)})


@app.route('/analyze/sentence', methods=['POST'])
@auth.login_required
def analyze_sentence():
    access = g.user.access.all()
    counter = 0
    for element in access:
        if element.path == '/analyze/sentence' and element.timeref >= int(time()) - 86400:
            counter = 1
    if counter == 0:
        abort(403)
    sentence = request.json.get('sentence')
    if sentence is None:
        abort(400)
    sentence = sentence.encode('utf8')
    sentenceAnalyzer = sentiment.SentenceSentimentAnalyzer()
    sentenceAnalyzer.load()
    results = sentenceAnalyzer.analyze(sentence)
    return jsonify({'Positif': round(results[2] * 100, 2),
                    'Neutre': round(results[1] * 100, 2),
                    'Negatif': round(results[0] * 100, 2)  })


@app.route('/analyze/text', methods=['POST'])
@auth.login_required
def analyze_text():
    access = g.user.access.all()
    counter = 0
    for element in access:
        if element.path == '/analyze/text' and element.timeref >= int(time()) - 86400:
            counter = 1
    if counter == 0:
        abort(403)
    text = request.json.get('text')
    if text is None:
        abort(400)
    text = text.encode('utf8')
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
    access = g.user.access.all()
    counter = 0
    for element in access:
        if element.path == '/analyze/customer' and element.timeref >= int(time()) - 86400:
            counter = 1
    if counter == 0:
        abort(403)
    sentence = request.json.get('sentence')
    if sentence is None:
        abort(400)
    sentence = sentence.encode('utf8')
    textCS = sentiment.CustomerServiceAnalyzer()
    textCS.load()
    results = textCS.analyze(sentence)
    return jsonify({'Sentiment': round(results[0] * 100, 2),
                    'Agressivite': round(results[1] * 100, 2),
                    'Remboursement': round(results[2] * 100, 2) })


@app.route('/image', methods=['POST'])
@auth.login_required
def image_analyzer():
    access = g.user.access.all()
    counter = 0
    for element in access:
        if element.path == '/image' and element.timeref >= int(time()) - 86400:
            counter = 1
    if counter == 0:
        abort(403)
    url = request.json.get('image-url')
    if url is None:
        abort(400)
    # get the image format
    reqst = urllib2.urlopen(url)
    mime = reqst.info()['Content-type']
    frmt = mime.split('/')[-1]
    # download the image
    if mime.endswith("jpeg"):
        image_name = 'database/image.jpg'
    else:
        image_name = 'database/image.' + frmt
    args = ['wget', '-O', image_name, url]
    subprocess.call(args)
    # Call the image analysis model
    imgClassifier = classifier.MultiLabelClassifier()
    imgClassifier.load()
    results = imgClassifier.classify( image_name, nbClasses=1000)
    data = {}
    for r in results:
    	if r[1] > 0.005:
            data[r[0]] = round((r[1] * 100), 2)
    # Delete the image after getting the analysis results
    subprocess.call(['rm', '-f', image_name])
    return jsonify(data)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    if not os.path.exists('database/db.sqlite'):
        InitializeDB(db)
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='0.0.0.0', debug=True)
