from ...aipcloud.text.sentiment import CustomerServiceAnalyzer
from flask import abort, jsonify

def analyzer(sentence):
    if sentence is None:
        abort(400)
    try:
        textCS = CustomerServiceAnalyzer()
        textCS.load()
        results = textCS.analyze(sentence)
        return jsonify({'Sentiment': round(results[0] * 100, 2),
                        'Agressivite': round(results[1] * 100, 2),
                        'Remboursement': round(results[2] * 100, 2) })
    except Exception as e:
        abort(500, e)
