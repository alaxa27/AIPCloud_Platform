#!/usr/bin/env python
# -*- coding: utf-8 -*
from src import app, auth
from src.authentication import Authentication
from flask import request, g, abort, json
from flask_cors import CORS, cross_origin
from src.access_points import init
from src.access_points import user as userAP
from src.access_points.analyze import image, sentence, text, dialogue, extraction, customer, intent, word
from src.access_points.analyze.sound import speech2text

CORS(app)

sentenceAnalyzer = None
textAnalyzer = None
dialogueAnalyzer = None
textCS = None
intentAnalyzer = None
keywords = None
speechClient = None


@auth.verify_password
def verify_password(email_or_token, password):
    authenticate = Authentication()
    return authenticate.verify_password(email_or_token, password)


@app.before_first_request
def initialization():
    global sentenceAnalyzer, textAnalyzer, dialogueAnalyzer, textCS, intentAnalyzer, keywords, speechClient
    sentenceAnalyzer, textAnalyzer, dialogueAnalyzer, intentAnalyzer, textCS, keywords, speechClient = init.initialize()

@app.route('/users/add', methods=['POST'])
@auth.login_required
def add_user():
    if not g.user.admin:
        abort(403, 'You are not an admin! Please contact Benjamin Dallard.')
    else:
        email = request.json.get('email')
        password = request.json.get('password')
        adminBool = request.json.get('admin')
        access_points = request.json.get('access_points')
        return userAP.add(email, password, adminBool, access_points)


@app.route('/token')
@auth.login_required
def get_auth_token():
    user = g.user
    return userAP.generate_token(user)


@app.route('/users/grant', methods=['POST'])
@auth.login_required
def grant_access():
    if not g.user.admin:
        abort(403, 'You are not an admin! Please contact Benjamin Dallard.')
    else:
        email = request.json.get('email')
        route = request.json.get('route')
        timeref = request.json.get('timeref')
    return userAP.grant(email, route, timeref)


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
    return sentence.analyzer(sent, sentenceAnalyzer)


@app.route('/analyze/text', methods=['POST'])
@auth.login_required
def analyze_text():
    g.user.verify_access('/analyze/text')
    t = request.json.get('text')
    return text.analyzer(t, textAnalyzer)


@app.route('/analyze/customer', methods=['POST'])
@auth.login_required
def customer_service_analyzer():
    g.user.verify_access('/analyze/customer')
    txt = request.json.get('text')
    return customer.analyzer(txt, textCS)

@app.route('/analyze/intent', methods=['POST'])
@auth.login_required
def intent_analyzer():
    g.user.verify_access('/analyze/intent')
    txt = request.json.get('text')
    return intent.analyzer(txt, intentAnalyzer)

@app.route('/analyze/dialogue', methods=['GET'])
@auth.login_required
def dialogue_analyzer():
    g.user.verify_access('/analyze/dialogue')
    return dialogue.analyzer(dialogueAnalyzer)


@app.route('/analyze/extraction', methods=['POST'])
@auth.login_required
def keywords_extraction():
    g.user.verify_access('/analyze/extraction')
    txt = request.json.get('text')
    sentimentBool = request.json.get('sentiment')
    volume = request.json.get('volume')
    return extraction.extract(txt, sentimentBool, volume, keywords, sentenceAnalyzer)


@app.route('/analyze/image', methods=['POST'])
@auth.login_required
def image_analyzer():
    g.user.verify_access('/analyze/image')
    url = request.json.get('image_url')
    return image.classify(url)

@app.route('/analyze/sound/speech2text', methods=['POST'])
@auth.login_required
def speech_to_text():
    g.user.verify_access('/analyze/sound/speech2text')
    url = request.json.get('audio_url')
    return speech2text.speech2text(url, speechClient)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
