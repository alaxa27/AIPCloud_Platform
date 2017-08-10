#!/usr/bin/env python
# -*- coding: utf-8 -*
from src import app, auth
from src.authentication import Authentication
from flask import request, g, abort
from flask_cors import CORS, cross_origin
from src.access_points import token, init, grantaccess
from src.access_points.analyze import image, sentence, text, dialogue, extraction, customer, word

CORS(app)

sentenceAnalyzer = None
textAnalyzer = None
dialogueAnalyzer = None
textCS = None
keywords = None


@auth.verify_password
def verify_password(email_or_token, password):
    authenticate = Authentication()
    return authenticate.verify_password(email_or_token, password)


@app.before_first_request
def initialization():
    global sentenceAnalyzer, textAnalyzer, dialogueAnalyzer, textCS, keywords
    sentenceAnalyzer, textAnalyzer, dialogueAnalyzer, textCS, keywords = init.initialize()


@app.route('/token')
@auth.login_required
def get_auth_token():
    user = g.user
    return token.generate_token(user)


@app.route('/grantaccess', methods=['POST'])
@auth.login_required
def grant_access():
    if not g.user.admin:
        abort(403, 'You are not an admin! Please contact Benjamin Dallard.')
    else:
        email = request.json.get('email')
        route = request.json.get('route')
    return grantaccess.grant(email, route)


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
    return extraction.extract(txt, sentimentBool, volume, keywords)


@app.route('/analyze/image', methods=['POST'])
@auth.login_required
def image_analyzer():
    g.user.verify_access('/analyze/image')
    url = request.json.get('image_url')
    return image.classify(url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
