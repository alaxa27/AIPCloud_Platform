from flask import abort, jsonify

def analyzer(text, textAnalyzer):
    if text is None:
        abort(400)
    try:
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
