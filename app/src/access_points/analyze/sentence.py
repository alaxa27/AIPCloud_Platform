from ...aipcloud.text.sentiment import SentenceSentimentAnalyzer
from flask import abort, jsonify

def analyzer(sentence):
    if sentence is None:
        abort(400)
    try:
        sentenceAnalyzer = SentenceSentimentAnalyzer()
        sentenceAnalyzer.load()
        results = sentenceAnalyzer.analyze(sentence)
        return jsonify({'Positif': round(results[2] * 100, 2),
                        'Neutre': round(results[1] * 100, 2),
                        'Negatif': round(results[0] * 100, 2)  })
    except Exception as e:
        abort(500, e)
