from flask import abort, g
from ..aipcloud.text import sentiment, extraction
from ..aipcloud.sound import Speech2Text
from ..aipcloud.sound.emotion import SpeechEmotionAnalyzer
from ..aipcloud.sound.clustering import SpeakerClusterAnalyzer
#from .. import db
#from ..initialize_db import InitializeDB

def initialize():
    #InitializeDB(db)
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
    intentAnalyzer = sentiment.IntentAnalyzer()
    intentAnalyzer.load()
    keywords = extraction.KeywordsExtraction()
    keywords.load()
    speechClient = Speech2Text()

    speechEmotionAnalyzer = SpeechEmotionAnalyzer()
    speechEmotionAnalyzer.load()
    speakerClusterAnalyzer = SpeakerClusterAnalyzer()
    speakerClusterAnalyzer.load()
    return sentenceAnalyzer, textAnalyzer, dialogueAnalyzer, intentAnalyzer, textCS, keywords, speechClient, speechEmotionAnalyzer, speakerClusterAnalyzer
