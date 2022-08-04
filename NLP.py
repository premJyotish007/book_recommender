import en_core_web_sm
from string import punctuation

# Natural Language Toolkit package
from nltk.corpus import wordnet
nlp = en_core_web_sm.load()

# IBM Watson package
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class Analyze:
    def __init__(self) -> None:
        self.authenticator = IAMAuthenticator("gBM315juVfKWlIiEzn4uNyvhIO3JVy3CKKR8hnWZfMlD")
        self.tone_analyzer = ToneAnalyzerV3(
            version='2017-09-21',
            authenticator=self.authenticator
        )

    def analyze_tone(self, text):
        print(text)
        self.tone_analyzer.set_service_url("https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/afd81026-a1c6-4e99-a7fb-cf368ae87909")
        tone_analysis = self.tone_analyzer.tone(
            {'text': text},
            content_type='application/json'
        ).get_result()
        result = []
        for i in range(len(tone_analysis["document_tone"]["tones"])):
            result.append((tone_analysis["document_tone"]["tones"][i]["score"], tone_analysis["document_tone"]["tones"][i]["tone_name"]))
        return result
    
    def get_keywords(self, text, types_tokens = ["NOUN"]):
        doc = nlp(text.lower())
        tokens = set()
        for token in doc:
            if (token.text not in nlp.Defaults.stop_words and token.text not in punctuation and token.pos_ in types_tokens):
                tokens.add(token.text)
        return list(tokens)

    
    
    