from flask import abort, jsonify, g

def analyzer(text, textAnalyzer):
    if text is None:
        abort(400)
    try:
        analysis = textAnalyzer.analyze(text, verbose=False)
        results = analysis.res
        data = {'positivity': round(results[2] * 100, 2),
                'neutrality': round(results[1] * 100, 2),
                'negativity': round(results[0] * 100, 2),
                'relevance': round(results[3] * 100, 2),
                'slope': round(results[4], 4),
                'lerp': round(results[5], 4),
                'variance': round(results[6], 4),
                'summary': textAnalyzer.summary(results) }
        g.user.save_query('/analyze/text', data)
        return jsonify(data)
    except Exception as e:
        abort(500, e)
