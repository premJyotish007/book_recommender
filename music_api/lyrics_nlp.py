import GeniusAPI
import en_core_web_sm
from string import punctuation

# Natural Language Toolkit imports
import nltk
from nltk.corpus import wordnet
nlp = en_core_web_sm.load()

from nltk.sentiment import SentimentIntensityAnalyzer

import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import sklearn


class LyricsNLP:
    def __init__(self, song, artist = "") -> None:
        self.song = song
        self.ls = GeniusAPI.LyricsScraper()
        self.lyrics = self.ls.get_lyrics(self.song, artist) if len(artist) > 0 else self.ls.get_lyrics(self.song)
        self.authenticator = IAMAuthenticator("gBM315juVfKWlIiEzn4uNyvhIO3JVy3CKKR8hnWZfMlD")
        self.tone_analyzer = ToneAnalyzerV3(
            version='2017-09-21',
            authenticator=self.authenticator
        )

    def analyze_tone(self):
        text = self.lyrics
        
        self.tone_analyzer.set_service_url("https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/afd81026-a1c6-4e99-a7fb-cf368ae87909")
        tone_analysis = self.tone_analyzer.tone(
            {'text': text},
            content_type='application/json'
        ).get_result()
        result = []
        for i in range(len(tone_analysis["document_tone"]["tones"])):
            result.append((tone_analysis["document_tone"]["tones"][i]["score"], tone_analysis["document_tone"]["tones"][i]["tone_name"]))
        return result
    
    def get_keywords(self, types_tokens = ["NOUN"]):
        doc = nlp(self.lyrics.lower())
        tokens = set()
        for token in doc:
            if (token.text not in nlp.Defaults.stop_words and token.text not in punctuation and token.pos_ in types_tokens):
                tokens.add(token.text)
        return list(tokens)



lnlp = LyricsNLP("Stan", "Eminem")
print(lnlp.analyze_tone())
print(lnlp.get_keywords())

    
    
    