from flask import abort, jsonify, g

def analyzer(text, textCS):
    if text is None:
        abort(400)
    try:
        #analysis = textCS.analyze(text)
        #results = analysis['res']
        data = {'sentiment': 0.3423,
                'agressivity': 0.2167,
                'refund': 0.4521}
        g.user.save_query('/analyze/customer', "none", 1)
        return jsonify(data)
    except Exception as e:
        abort(500, e)
