from flask import abort, jsonify


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

        keywords = keywords.extract(text, keywordCount=volume, verbose=True)
        data = []
        for key in keywords:
            if  sentimentBool:
                if int(sentimentBool):
                    #callsentiment

                    data.append({"keyword": key[0], "score": round(key[1], 4), "sentiment": {
                        "positivity": 45.7,
                        "neutrality": 39,
                        "negativity": 15.3,
                        "relevance": 62.6

                    }})
                    #Get sentiment from eachword
                    pass
            else:
                data.append({"keyword": key[0], "score": round(key[1], 4)})

        return jsonify(data)
    except Exception as e:
        abort(500, e)
