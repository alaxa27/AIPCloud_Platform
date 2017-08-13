from flask import abort, jsonify, g


def extract(text, sentimentBool, volume, keywords, sentenceAnalyzer):
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
                    analysis = sentenceAnalyzer.analyze(key[0])
                    results = analysis['res']

                    data.append({"keyword": key[0], "score": round(key[1], 4), "sentiment": {
                        "positivity": str(round(results[2], 4)),
                        "neutrality": str(round(results[1], 4)),
                        "negativity": str(round(results[0], 4))

                    }})
                    #Get sentiment from eachword
                    pass
            else:
                data.append({"keyword": key[0], "score": round(key[1], 4)})
        g.user.save_query('/analyze/extraction', data, analysis['exec_time'])
        return jsonify(data)
    except Exception as e:
        abort(500, e)
