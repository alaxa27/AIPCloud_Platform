from flask import abort, jsonify, g

def analyzer(text, textCS):
    if text is None:
        abort(400)
    try:
        analysis = textCS.analyze(text)
        results = analysis['res']
        data = {'sentiment': round(results[0] * 100, 2),
                'agressivite': round(results[1] * 100, 2),
                'remboursement': round(results[2] * 100, 2) }
        g.user.save_query('/analyze/customer', analysis)
        return jsonify(data)
    except Exception as e:
        abort(500, e)
