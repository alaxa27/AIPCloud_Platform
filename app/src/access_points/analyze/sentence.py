from flask import abort, jsonify, g


def analyzer(sentence, sentenceAnalyzer):
    if sentence is None or len(sentence.split()) == 0:
        abort(400)
    try:
        analysis = sentenceAnalyzer.analyze(sentence)
        results = analysis['res']
        data = {'positivity': float(round(results[2], 4)),
                'neutrality': float(round(results[1], 4)),
                'negativity': float(round(results[0], 4))}
        g.user.save_query('/analyze/sentence', data, analysis['exec_time'])
        return jsonify(data)
    except Exception as e:
        abort(500, e)
