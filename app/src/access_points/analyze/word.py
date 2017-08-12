from ...aipcloud.text import sentiment
from flask import abort, jsonify, g


def analyzer(word):
    if word is None:
        abort(400)
    try:
        wordAnalyzer = sentiment.WordSentimentAnalyzer()
        wordAnalyzer.load()
        results = wordAnalyzer.analyze(word, verbose=False)
        data = {'positivity': round(results[2] * 100, 2),
                'neutrality': round(results[1] * 100, 2),
                'negativity': round(results[0] * 100, 2),
                'relevance': round(results[3] * 100, 2)
                }
        g.user.save_query('/analyze/word', data)
        return jsonify(data)
    except Exception as e:
        abort(500, e)
