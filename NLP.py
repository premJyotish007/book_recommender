import en_core_web_sm
from string import punctuation

# Natural Language Toolkit package
from nltk.corpus import wordnet
nlp = en_core_web_sm.load()

# IBM Watson package
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, KeywordsOptions, SentimentOptions, EmotionOptions


class Analyze:
    def __init__(self, apikey = "E6i0jHhpPoElqlwbtvKR0pTZd23TpMn37f2-cLbbZGV6",
                        url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/3e31fa36-c54a-4080-9f19-2d089abf8da8") -> None:
        self.authenticator = IAMAuthenticator(apikey)
        self.natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2022-04-07',
            authenticator=self.authenticator
        )
        self.natural_language_understanding.set_service_url(url)


    def analyze(self, text):
        try:
            response = self.natural_language_understanding.analyze(
            text = text,
            features = Features(emotion = EmotionOptions())).get_result()
            emotions_dict = response["emotion"]["document"]["emotion"]
            return [[emotion, score] for emotion, score in emotions_dict.items()]
        except:
            return [[], []]
    
    def get_keywords(self, text, types_tokens = ["NOUN"]):
        doc = nlp(text.lower())
        tokens = set()
        for token in doc:
            if (token.text not in nlp.Defaults.stop_words and token.text not in punctuation and token.pos_ in types_tokens):
                tokens.add(token.text)
        response = self.natural_language_understanding.analyze(
            text = text,
            features = Features(keywords = KeywordsOptions())).get_result()
        return set([keyword["text"] for keyword in response["keywords"]] + list(tokens))
    
    