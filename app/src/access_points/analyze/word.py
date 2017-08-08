from ...aipcloud.text import sentiment
from flask import abort, jsonify


def analyzer(word):
    if word is None:
        abort(400)
    try:
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
