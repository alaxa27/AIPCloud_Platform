from flask import abort, jsonify

def analyzer(text, textCS):
    if text is None:
        abort(400)
    try:
        results = textCS.analyze(text)
        return jsonify({'Sentiment': round(results[0] * 100, 2),
                        'Agressivite': round(results[1] * 100, 2),
                        'Remboursement': round(results[2] * 100, 2) })
    except Exception as e:
        abort(500, e)
