from flask import abort, jsonify, g


def analyzer(sentence, sentenceAnalyzer):
    if sentence is None:
        abort(400)
    try:
        analysis = sentenceAnalyzer.analyze(sentence)
        results = analysis['res']
        data = {'positif': round(results[2] * 100, 2),
                'neutre': round(results[1] * 100, 2),
                'negatif': round(results[0] * 100, 2)}
        g.user.save_query('/analyze/sentence', data, analysis['exec_time'])
        return jsonify(data)
    except Exception as e:
        abort(500, e)
