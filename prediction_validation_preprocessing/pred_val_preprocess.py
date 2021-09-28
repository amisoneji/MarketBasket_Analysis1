from sklearn.feature_extraction.text import CountVectorizer

import unicodedata2
from nltk import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from application_logging import logger
from nltk.stem import WordNetLemmatizer
import string
from gevent.pywsgi import WSGIServer
from gensim.models import Word2Vec, KeyedVectors
from gensim.test.utils import datapath, get_tmpfile
from gensim.scripts.glove2word2vec import glove2word2vec

from nltk.stem.porter import *
from file_operations import file_methods


class pre_prediction:
    def __init__(self):
        self.log_writer = logger.App_Logger()
        self.file_object=open("Prediction_Logs/Prediction_Log.txt", 'a+')


    def tokenizations(self,data):
        self.log_writer.log(self.file_object, 'start of tokenization')
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
                        ss = ss.strip()
                return ss

            data=text_cleaning(data)
            print(data)
            return data

        except Exception as e:
            self.log_writer.log(self.file_object,
                                   'Exception occured in tokenizations method of the pre_prediction class. Exception message:  ' + str(
                                       e))
            raise Exception()





