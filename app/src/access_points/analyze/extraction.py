from flask import abort, jsonify, g


def extract(text, sentimentBool, volume, keywords):
    try:
        if text is None:
            abort(400)
        if volume is None:
            volume = 8
        else:
            volume = float(volume)
        if sentimentBool:
            sentimentBool = int(sentimentBool)

        analysis = keywords.extract(text, keywordCount=volume, verbose=True)
        keywords = analysis['res']
        data = []
        for key in keywords:
            if  sentimentBool:
                if int(sentimentBool):
                    #callsentiment

                    data.append({"keyword": key[0], "score": round(key[1], 4), "sentiment": {
                        "positivity": 0,
                        "neutrality": 100,
                        "negativity": 0,
                        "relevance": 62.6

                    }})
                    #Get sentiment from eachword
                    pass
            else:
                data.append({"keyword": key[0], "score": round(key[1], 4)})
        g.user.save_query('/analyze/extraction', data)
        return jsonify(data)
    except Exception as e:
        abort(500, e)
