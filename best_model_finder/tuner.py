from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import BernoulliNB
#from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.model_selection  import GridSearchCV

class Model_Finder:
    """
                This class shall  be used to find the model with best accuracy and AUC score.
                Written By: iNeuron Intelligence
                Version: 1.0
                Revisions: None
                """
    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.knn = KNeighborsClassifier()
        self.bernouli = BernoulliNB()

    def get_best_params_for_KNN(self, train_x, train_y):
        """
                                                Method Name: get_best_params_for_KNN
                                                Description: get the parameters for KNN Algorithm which give the best accuracy.
                                                             Use Hyper Parameter Tuning.
                                                Output: The model with the best parameters
                                                On Failure: Raise Exception
                                        """
        self.logger_object.log(self.file_object,
                               'Entered the get_best_params_for_Ensembled_KNN method of the Model_Finder class')
        try:
            # initializing with different combination of parameters
            self.param_grid_knn = {
                'algorithm': ['ball_tree', 'kd_tree'],
                'leaf_size': [10, 17, 24],
                'n_neighbors': [4, 5, 8],
                'p': [1]
            }
            # Creating an object of the Grid Search class
            self.grid = GridSearchCV(self.knn, self.param_grid_knn, verbose=3,
                                     cv=3)
            # finding the best parameters
            self.grid.fit(train_x, train_y)
            # extracting the best parameters
            self.algorithm = self.grid.best_params_['algorithm']
            self.leaf_size = self.grid.best_params_['leaf_size']
            self.n_neighbors = self.grid.best_params_['n_neighbors']
            self.p = self.grid.best_params_['p']
            # creating a new model with the best parameters
            self.knn = KNeighborsClassifier(algorithm=self.algorithm, leaf_size=self.leaf_size,
                                            n_neighbors=self.n_neighbors, p=self.p)
            # training the mew model
            self.knn.fit(train_x, train_y)
            self.logger_object.log(self.file_object,
                                   'KNN best params: ' + str(
                                       self.grid.best_params_) + '. Exited the KNN method of the Model_Finder class')
            return self.knn

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in knn method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'knn Parameter tuning  failed. Exited the knn method of the Model_Finder class')
            raise Exception()

    def model_BernoulliNB(self, train_x, train_y):
        """"

                                Method Name: model_BernoulliNB
                                Description: fit BernoulliNB model for data
                                Output: model
                                On Failure: Raise Exception

                                Written By: Ami


        """
        self.logger_object.log(self.file_object, 'Entered the model_BernoulliNB method of the Model_Finder class')
        try:
            self.bernouli = BernoulliNB()
            self.bernouli.fit(train_x, train_y)
            print("bernoli done")
            return self.bernouli
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in model_BernoulliNB of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'model_BernoulliNB  failed. Exited the get_best_params_for_random_forest method of the Model_Finder class')
            raise Exception()

    # def get_best_params_for_logistic(self, train_x, train_y):
    #     """
    #                                             Method Name: get_best_params_for_KNN
    #                                             Description: get the parameters for KNN Algorithm which give the best accuracy.
    #                                                          Use Hyper Parameter Tuning.
    #                                             Output: The model with the best parameters
    #                                             On Failure: Raise Exception
    #                                     """
    #     self.logger_object.log(self.file_object,
    #                            'Entered the logistic best parametr finding method of the Model_Finder class')
    #     try:
    #         # initializing with different combination of parameters
    #         self.param_grid_logi = {
    #             "solver" : ["lbfgs", "liblinear","sag"],
    #             "penalty" : ["none", "l1","l2", "elasticnet"],
    #             "C" :[50,10, 1.0, 0.1, 0.01]
    #         }
    #         # Creating an object of the Grid Search class
    #         self.grid = GridSearchCV(self.logi, self.param_grid_logi, verbose=3,
    #                                  cv=3)
    #         # finding the best parameters
    #         self.grid.fit(train_x, train_y)
    #         # extracting the best parameters
    #         self.solver = self.grid.best_params_['solver']
    #         self.penalty = self.grid.best_params_['penalty']
    #         self.C = self.grid.best_params_['C']
    #
    #         # creating a new model with the best parameters
    #         self.logi = LogisticRegression(solver=self.solver, penalty=self.penalty, C=self.C)
    #         # training the mew model
    #         self.logi.fit(train_x, train_y)
    #         self.logger_object.log(self.file_object,
    #                                'logistic best params: ' + str(
    #                                    self.grid.best_params_) + '. Exited the logistic method of the Model_Finder class')
    #         return self.logi

        # except Exception as e:
        #     self.logger_object.log(self.file_object,
        #                            'Exception occured in logistic method of the Model_Finder class. Exception message:  ' + str(
        #                                e))
        #     self.logger_object.log(self.file_object,
        #                            'logistic Parameter tuning  failed. Exited the logistic method of the Model_Finder class')
        #     raise Exception()



    def get_best_model(self,train_x,train_y,test_x,test_y):
        """
                                                Method Name: get_best_model
                                                Description: Find out the Model which has the best AUC score.
                                                Output: The best model name and the model object
                                                On Failure: Raise Exception

                                                Written By: Ami


                                   """
        self.logger_object.log(self.file_object,
                               'Entered the get_best_model method of the Model_Finder class')
        # create best model for KNN

# 'numpy.ndarray' object has no attribute 'unique'

        try:
            # self.mul_bn = MultinomialNB()
            # self.mul_bn.fit(train_x, train_y)

            self.knn = self.get_best_params_for_KNN(train_x, train_y)
            print("1")
            #self.mul_bn.fit(train_x, train_y)
            self.prediction_knn = self.knn.predict_proba(test_x)
            print((self.prediction_knn).shape)
            print((test_x).shape)
            (unique, counts) = np.unique(test_y, return_counts=True)

            print(counts)
            print()
            #if (len(unique)) == 1: #if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                #print("*")
                #self.knn_score = accuracy_score(test_y, self.prediction_knn)
                #print("4")
                #self.logger_object.log(self.file_object, 'Accuracy for KNeighborsClassifier:' + str(self.knn_score))
                #print("5")# Log AUC

            self.knn_score = roc_auc_score(test_y, self.prediction_knn, multi_class='ovr') # AUC for KNN
            print("6")
            self.logger_object.log(self.file_object, 'Accuracy for KNeighborsClassifier:' + str(self.knn_score ))
            print("7")# Log AUC

            self.bernouli = self.model_BernoulliNB(train_x, train_y)
            self.prediction_bernouli = self.bernouli.predict_proba(test_x)

            if len(unique) == 1:  # if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.bernouli_score = accuracy_score(test_y, self.prediction_bernouli)
                self.logger_object.log(self.file_object,
                                       'Accuracy for bernouli:' + str(self.bernouli_score))  # Log AUC
            else:
                self.bernouli_score = roc_auc_score(test_y, self.prediction_bernouli, multi_class='ovr')  # AUC for KNN
                self.logger_object.log(self.file_object,
                                       'Accuracy for bernouli:' + str(self.bernouli_score))  # Log AUC


            # self.logi = self.get_best_params_for_logistic(train_x, train_y)
            # print("8")
            # self.prediction_logi = self.logi.predict_proba(test_x)
            # print("9")
            #
            #
            # self.logi_score = roc_auc_score(test_y, self.prediction_logi, multi_class='ovr')  # AUC for KNN
            # print("12")
            # self.logger_object.log(self.file_object,
            #                        'Accuracy for logistic:' + str(self.logi_score ))
            # print("13")# Log AUC

            if (self.knn_score < self.bernouli_score):
                return 'bernoli', self.bernouli_score
            else:
                return 'KNeighborsClassifier', self.knn





        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_best_model method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Model Selection Failed. Exited the get_best_model method of the Model_Finder class')
            raise Exception()
