from flask import abort, g
from ..aipcloud.text import sentiment
# from . import db
# from .initialize_db import InitializeDB

def initialize():
    # InitializeDB(db)
    # The database is already initialized
    import nltk
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("averaged_perceptron_tagger")
    sentenceAnalyzer = sentiment.SentenceSentimentAnalyzer()
    sentenceAnalyzer.load()
    textAnalyzer = sentiment.TextSentimentAnalyzer()
    textAnalyzer.load()
    dialogueAnalyzer = sentiment.DialogueSentimentAnalyzer()
    dialogueAnalyzer.load()
    textCS = sentiment.CustomerServiceAnalyzer()
    textCS.load()
    return sentenceAnalyzer, textAnalyzer, dialogueAnalyzer, textCS
