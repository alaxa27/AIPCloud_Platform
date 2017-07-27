try:
        import nltk
        nltk.word_tokenize("test")
except :
        import nltk
        print("Downloading")
        nltk.download("all")
