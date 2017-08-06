from flask import g

from src.aipcloud.text import sentiment, extraction

def load_keywords_instance():
    keywords = getattr(g, '_keywords', None)
    if keywords is None:
        keywords = g._keywords = extraction.KeywordExtraction()
        keywords.load()
    return keywords

def load_keywords_instance():
    textAnalyzer = getattr(g, '_textAnalyzer', None)
    if textAnalyzer is None:
        textAnalyzer = g._textAnalyzer = sentiment.TextSentimentAnalyzer()
        textAnalyzer.load()
    return textAnalyzer
