from flask import abort, jsonify, g


def analyzer(sentence, sentenceAnalyzer):
    if sentence is None:
        abort(400)
    try:
        analysis = sentenceAnalyzer.analyze(sentence)
        results = analysis['res']
        data = {'positivity': str(round(results[2], 4)),
                'neutrality': str(round(results[1], 4)),
                'negativity': str(round(results[0], 4))}
        g.user.save_query('/analyze/sentence', data, analysis['exec_time'])
        return jsonify(data)
    except Exception as e:
        abort(500, e)
