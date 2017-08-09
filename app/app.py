#!/usr/bin/env python
# -*- coding: utf-8 -*
from src import app, auth
from src.authentication import Authentication
from flask import request, g
from flask_cors import CORS, cross_origin
from src.access_points import token, init
from src.access_points.analyze import image, sentence, text, dialogue, extraction, customer, word
from src.aipcloud.text import sentiment

CORS(app)

sentenceAnalyzer = None
textAnalyzer = None
dialogueAnalyzer = None
textCS = None


@auth.verify_password
def verify_password(email_or_token, password):
    authenticate = Authentication()
    return authenticate.verify_password(email_or_token, password)


@app.before_first_request
def initialization():
    global sentenceAnalyzer, textAnalyzer, dialogueAnalyzer, textCS
    sentenceAnalyzer, textAnalyzer, dialogueAnalyzer, textCS = init.initialize()


@app.route('/token')
@auth.login_required
def get_auth_token():
    user = g.user
    return token.generate_token(user)


@app.route('/analyze/word', methods=['POST'])
@auth.login_required
def analyze_word():
    g.user.verify_access('/analyze/word')
    w = request.json.get('word')
    return word.analyzer(w)


@app.route('/analyze/sentence', methods=['POST'])
@auth.login_required
def analyze_sentence():
    g.user.verify_access('/analyze/sentence')
    sent = request.json.get('sentence')
    global sentenceAnalyzer
    return sentence.analyzer(sent, sentenceAnalyzer)


@app.route('/analyze/text', methods=['POST'])
@auth.login_required
def analyze_text():
    g.user.verify_access('/analyze/text')
    t = request.json.get('text')
    global textAnalyzer
    return text.analyzer(t, textAnalyzer)


@app.route('/analyze/customer', methods=['POST'])
@auth.login_required
def customer_service_analyzer():
    g.user.verify_access('/analyze/customer')
    sent = request.json.get('sentence')
    global textCS
    return customer.analyzer(sent, textCS)


@app.route('/analyze/dialogue', methods=['GET'])
@auth.login_required
def dialogue_analyzer():
    g.user.verify_access('/analyze/dialogue')
    global dialogueAnalyzer
    return dialogue.analyzer(dialogueAnalyzer)


@app.route('/analyze/extraction', methods=['POST'])
@auth.login_required
def keywords_extraction():
    g.user.verify_access('/analyze/extraction')
    txt = request.json.get('text')
    sentimentBool = request.json.get('sentiment')
    volume = request.json.get('volume')
    return extraction.extract(txt, sentimentBool, volume)


@app.route('/analyze/image', methods=['POST'])
@auth.login_required
def image_analyzer():
    g.user.verify_access('/analyze/image')
    url = request.json.get('image_url')
    return image.classify(url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
