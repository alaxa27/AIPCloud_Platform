from flask import abort, jsonify

def analyzer(sentence, textCS):
    if sentence is None:
        abort(400)
    try:
        results = textCS.analyze(sentence)
        return jsonify({'Sentiment': round(results[0] * 100, 2),
                        'Agressivite': round(results[1] * 100, 2),
                        'Remboursement': round(results[2] * 100, 2) })
    except Exception as e:
        abort(500, e)
