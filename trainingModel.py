from sklearn.model_selection import train_test_split
from data_ingestion import data_loader
from data_preprocessing import preprocessing
from data_preprocessing import clustering
from best_model_finder import tuner
from sklearn.feature_extraction.text import CountVectorizer

from file_operations import file_methods
from application_logging import logger
from data_preprocessing import tokenazation
import numpy as np
import joblib


class trainModel:

    def __init__(self):
        self.log_writer = logger.App_Logger()
        self.file_object = open("Training_Logs/ModelTrainingLog.txt", 'a+')

    def trainingModel(self):
        # Logging the start of Training
        self.log_writer.log(self.file_object, 'Start of Training')

        try:
            # Getting the data from the source
            data_getter = data_loader.Data_Getter(self.file_object, self.log_writer)
            data = data_getter.get_data()

            """doing the data preprocessing"""

            preprocessor = preprocessing.Preprocessor(self.file_object, self.log_writer)


            # removing unwanted columns as discussed in the EDA part in ipynb file
            df = preprocessor.remove_columns(data, ['review_id', 'order_id', 'review_score', 'review_comment_title',
                                                    'review_creation_date', 'review_answer_timestamp'])
            self.log_writer.log(self.file_object, '1 remove column completed--of Training')

            preprocessor.DropNullValues(df)

            df = preprocessor.getNecessaryColumn(df, "review_comment_message")

            tokenize = tokenazation.Tokenize(self.file_object, self.log_writer)
            final_corpus = tokenize.corpus_finding(df)
            final_corpus=final_corpus[0:30000]
            print("*")

            self.log_writer.log(self.file_object, '4 final corpus created End of Training')
            vectorizer = CountVectorizer(ngram_range=(1,2))
            X = vectorizer.fit_transform(final_corpus)
            X = X.toarray()

            self.log_writer.log(self.file_object, 'tokenize corpus created')

            """ Applying the clustering approach"""

            kmeans = clustering.KMeansClustering(self.file_object, self.log_writer)  # object initialization.
            number_of_clusters = kmeans.elbow_plot(X)  # using the elbow plot to find the number of optimum clusters

            # creating clusters the data into clusters
            y = kmeans.create_clusters(X, 9)


            x_train, x_test, y_train, y_test = train_test_split(X, y,random_state=42)
            print("splitting done")
            print("clustring done")




            model_finder = tuner.Model_Finder(self.file_object, self.log_writer)  # object initialization

            # getting the best model for each of the clusters
            best_model_name, best_model = model_finder.get_best_model(x_train, y_train, x_test, y_test)

            # saving the best model to the directory.

            joblib.dump(best_model, f"{best_model_name}.model")
            joblib.dump(vectorizer,"vectorizer.model")
            self.log_writer.log(self.file_object, 'Successful End of Training')
            self.file_object.close()

        except Exception:
            # logging the unsuccessful Training
            self.log_writer.log(self.file_object, 'Unsuccessful End of Training')
            self.file_object.close()
            raise Exception
