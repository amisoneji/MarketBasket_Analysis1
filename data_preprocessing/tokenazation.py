
import unicodedata2
from nltk import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from nltk.stem import WordNetLemmatizer
import string
from sklearn.feature_extraction.text import CountVectorizer


class Tokenize:
    """
            This class shall  be used to tokenize words from reviews.

            Written By: Ami Soneji
            Version: 1.0
            Revisions: None

            """

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object



    def corpus_finding(self,data):
        self.logger_object.log(self.file_object, 'Entered the text_cleaning method of the tokenize class')
        self.data=data
        try:
            def text_cleaning(doc):
                def remove_accents(text):
                    return unicodedata2.normalize('NFKD', text).encode('ascii', errors='ignore').decode('utf-8')

                STOP_WORDS = set(remove_accents(w) for w in stopwords.words('portuguese'))
                STOP_WORDS.remove('nao')  # This word is key to understand delivery problems later

                wnl = WordNetLemmatizer()
                doc = doc.lower()
                doc = re.sub(f"[{string.punctuation}]", "", doc)
                ss = ""
                for w in word_tokenize(doc):
                    if (w not in STOP_WORDS):
                        ss = ss + " " + wnl.lemmatize(w)
                        ss=ss.strip()
                return ss

            data=data.apply(text_cleaning)
            return data

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in text_cleaning method of the tokenize class. Exception message:  ' + str(e))
            raise Exception()




