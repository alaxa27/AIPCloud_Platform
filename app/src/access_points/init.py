from flask import abort, g
from ..aipcloud.text import sentiment, extraction
# from .. import db
# from ..initialize_db import InitializeDB

def initialize():
    # InitializeDB(db)
    # The database is already initialized
    import nltk
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("averaged_perceptron_tagger")
    sentenceAnalyzer = sentiment.SentenceSentimentAnalyzer()
    sentenceAnalyzer.load()
    textAnalyzer = sentiment.TextSentimentAnalyzer(analyzer=sentenceAnalyzer)
    textAnalyzer.load()
    dialogueAnalyzer = sentiment.DialogueSentimentAnalyzer(analyzer=sentenceAnalyzer)
    dialogueAnalyzer.load()
    textCS = sentiment.CustomerServiceAnalyzer(sentimentAnalyzer=sentenceAnalyzer)
    textCS.load()
    keywords = extraction.KeywordExtraction()
    keywords.load()
    return sentenceAnalyzer, textAnalyzer, dialogueAnalyzer, textCS, keywords
