from flask import abort, jsonify, g

def analyzer(text, intentAnalyzer):
    if text is None:
        abort(400)
    try:
        analysis = intentAnalyzer.analyze(text)
        results = analysis['res']
        data = {
        'request': float(round(results[0], 4)),
        'threat': float(round(results[1], 4)),
        'opinion': float(round(results[2], 4))
        }
        g.user.save_query('/analyze/intent', data, anlaysys['exec_time'])
        return jsonify(data)
    except Exception as e:
        abort(500, e)
