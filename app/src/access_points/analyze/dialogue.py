from flask import abort, jsonify
from ...snippets.snippets import dialA, dialB

def analyzer(dialogueAnalyzer):
    try:
        resultsA, resultsB, estim = dialogueAnalyzer.analyze(dialB, dialA, verbose=False)
        return jsonify({"Positif A": round(resultsA[2] * 100, 2),
                        "Neutre A": round(resultsA[1] * 100, 2),
                        "Negatif A": round(resultsA[0] * 100, 2),
                        "Pertinence A": round(estim[0] * 100, 2),
                        "Pente A": round(estim[3], 4),
                        "Positif B": round(resultsB[2] * 100, 2),
                        "Neutre B": round(resultsB[1] * 100, 2),
                        "Negatif B": round(resultsB[0] * 100, 2),
                        "Pertinence B": round(estim[1] * 100, 2),
                        "Pente B": round(estim[4], 4),
                        "Pertinence totale": round(estim[2] * 100, 2)})
    except Exception as e:
        abort(500, e)
