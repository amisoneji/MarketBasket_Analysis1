import pandas as pd
import numpy as np





class Preprocessor:
    """
        This class shall  be used to clean and transform the data before training.

        Written By: Ami Soneji
        Version: 1.0
        Revisions: None

        """

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def remove_columns(self,data,columns):
        """
                Method Name: remove_columns
                Description: This method removes the given columns from a pandas dataframe.
                Output: A pandas DataFrame after removing the specified columns.
                On Failure: Raise Exception

                Written By: Ami Soneji
                Version: 1.0
                Revisions: None

        """
        self.logger_object.log(self.file_object, 'Entered the remove_columns method of the Preprocessor class')
        self.data=data
        self.columns=columns
        try:
            self.data=self.data.drop(labels=self.columns, axis=1) # drop the labels specified in the columns
            self.logger_object.log(self.file_object,
                                   'Column removal Successful.Exited the remove_columns method of the Preprocessor class')
            return self.data
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in remove_columns method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,
                                   'Column removal Unsuccessful. Exited the remove_columns method of the Preprocessor class')
            raise Exception()

    def getNecessaryColumn(self, data, NameofColumn):
        """

        Description: This methoddrops wanted columns that are  used ofor analysis

        Written
        By: Ami Soneji

         """

        try:

            self.logger_object.log(self.file_object, 'Entered the getNecessaryColumn method of the Preprocessor class')

            self.data = data
            self.NameofColumn=NameofColumn
            data=data[NameofColumn]
            return data


        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in drop getNecessaryColumn of the Preprocessor class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Finding getNecessaryColumn Exited the getNecessaryColumn method of the Preprocessor class')
            raise Exception()









    def DropNullValues(self,data):
        """


        Method Name: DropNullValues
        Description: This method drop null values for column which we required
        Written By: Ami Soneji
        Version: 1.0
        Revisions: None
        """


        try:
            self.logger_object.log(self.file_object, 'Entered the DropNullValues method of the Preprocessor class')
            self.data.dropna( inplace=True)

            return self.data

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in drop null value method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,'Finding rop null value failed. Exited the is_null_present method of the Preprocessor class')
            raise Exception()



