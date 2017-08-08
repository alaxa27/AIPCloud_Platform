#!/usr/bin/env python
# -*- coding: utf-8 -*
from src import app, auth
from src.authentication import Authentication
# from src import db
# from src.initialize_db import InitializeDB
from src.snippets.snippets import dialA, dialB
from flask import abort, request, jsonify, g
from flask_cors import CORS, cross_origin
from src.aipcloud.text import sentiment, extraction
from src.access_points import token
from src.access_points.analyze import image, sentence, text, dialogue, extraction, customer

from instances_aipcloud import load_keywords_instance, load_textAnalyzer_instance

CORS(app)


@auth.verify_password
def verify_password(email_or_token, password):
    authenticate = Authentication()
    return authenticate.verify_password(email_or_token, password)


@app.route('/init')
def initialization():
    try:
        # InitializeDB(db)
        # The database is already initialized
        import nltk
        nltk.download("punkt")
        nltk.download("stopwords")
        nltk.download("averaged_perceptron_tagger")
        return "200"
    except:
        return "400"


@app.route('/token')
@auth.login_required
def get_auth_token():
    user = g.user
    return token.generate_token(user)


@app.route('/analyze/word', methods=['POST'])
@auth.login_required
def analyze_word():
    try:
        user = g.user
        user.verify_access('/analyze/word')
        word = request.json.get('word')
        if word is None:
            abort(400)
        wordAnalyzer = sentiment.WordSentimentAnalyzer()
        wordAnalyzer.load()
        results = wordAnalyzer.analyze(word, verbose=False)
        return jsonify({'positivity': round(results[2] * 100, 2),
                        'neutrality': round(results[1] * 100, 2),
                        'negativity': round(results[0] * 100, 2),
                        'relevance': round(results[3] * 100, 2)
                        })
    except Exception as e:
        abort(500, e)

@app.route('/analyze/sentence', methods=['POST'])
@auth.login_required
def analyze_sentence():
    g.user.verify_access('/analyze/sentence')
    sent = request.json.get('sentence')
    return sentence.analyzer(sent)


@app.route('/analyze/text', methods=['POST'])
@auth.login_required
def analyze_text():
    g.user.verify_access('/analyze/text')
    text = request.json.get('text')
    try:
        if text is None:
            abort(400)
        textAnalyzer = load_textAnalyzer_instance()
        results = textAnalyzer.analyze(text, verbose=False)
        return jsonify({'positivity': round(results[2] * 100, 2),
                        'neutrality': round(results[1] * 100, 2),
                        'negativity': round(results[0] * 100, 2),
                        'relevance': round(results[3] * 100, 2),
                        'slope': round(results[4], 4),
                        'lerp': round(results[5], 4),
                        'variance': round(results[6], 4),
                        'summary': textAnalyzer.summary(results)})
    except Exception as e:
        abort(500, e)


@app.route('/analyze/customer', methods=['POST'])
@auth.login_required
def customer_service_analyzer():
    g.user.verify_access('/analyze/customer')
    sent = request.json.get('sentence')
    return customer.analyzer(sent)


@app.route('/analyze/dialogue', methods=['GET'])
@auth.login_required
def dialogue_analyzer():
    g.user.verify_access('/analyze/dialogue')
    return dialogue.analyzer()


@app.route('/analyze/extraction', methods=['POST'])
@auth.login_required
def keywords_extraction():
    try:
        user = g.user
        user.verify_access('/analyze/extraction')
        text = request.json.get('text')
        sentimentBool = request.json.get('sentiment')
        volume = request.json.get('volume')
        if text is None:
            abort(400)
        if volume is None:
            volume = 8
        else:
            volume = float(volume)
        if sentimentBool:
            sentimentBool = int(sentimentBool)

        keywords = load_keywords_instance()
        keywords = keywords.extract(text, keywordCount=volume, verbose=True)
        data = []
        for key in keywords:
            if  sentimentBool:
                if int(sentimentBool):
                    #callsentiment

                    data.append({"keyword": key[0], "score": round(key[1], 4), "sentiment": {
                        "positivity": 45.7,
                        "neutrality": 39,
                        "negativity": 15.3,
                        "relevance": 62.6

                    }})
                    #Get sentiment from eachword
                    pass
            else:
                data.append({"keyword": key[0], "score": round(key[1], 4)})

        return jsonify(data)
    except Exception as e:
        abort(500, e)


@app.route('/analyze/image', methods=['POST'])
@auth.login_required
def image_analyzer():
    g.user.verify_access('/analyze/image')
    url = request.json.get('image-url')
    return image.classify(url)


if __name__ == '__main__':
    import nltk
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("averaged_perceptron_tagger")
    app.run(host='0.0.0.0', debug=True)
