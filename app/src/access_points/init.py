def initialize():
    try:
        # InitializeDB(db)
        # The database is already initialized
        import nltk
        nltk.download("punkt")
        nltk.download("stopwords")
        nltk.download("averaged_perceptron_tagger")
        return "200"
    except:
        return "400"
