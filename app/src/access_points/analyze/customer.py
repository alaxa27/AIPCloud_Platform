from flask import abort, jsonify, g

def analyzer(text, textCS):
    if text is None:
        abort(400)
    try:
        analysis = textCS.analyze(text)
        results = analysis['res']
        data = {
        'satisfaction': float(round(results[0], 4)),
        'agressivity': float(round(results[1], 4)),
        'refund': float(round(results[2], 4))
        }
        g.user.save_query('/analyze/customer', data, analysis['exec_time'])
        return jsonify(data)
    except Exception as e:
        abort(500, e)
