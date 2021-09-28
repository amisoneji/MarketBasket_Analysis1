import shutil
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from os import listdir
import os
import csv
from application_logging.logger import App_Logger


class dBOperation:
    """
      This class shall be used for handling all the SQL operations.

      Written By: Ami Soneji
      Version: 1.0
      Revisions: None

      """
    def __init__(self):
        self.path = 'Training_Database/'
        self.badFilePath = "Training_Raw_files_validated/Bad_Raw"
        self.goodFilePath = "Training_Raw_files_validated/Good_Raw"
        self.logger = App_Logger()
        self.Client_id = 'fodmZDYoEBLtBFGqXNlubqIA'
        self.Client_secret = 'nhUH0AM5nr64jfShRKJ+,CvAki9_b1cxhnBH+vFKmSwvv,LM4IighDL2,afGOCei_vMM1axRLKNB9taxIhvdq8sZJgMwWq+Pgg85y,oJYt3JqGkwqmDbiLayyP9vN2,y'
        cloud_config = {'secure_connect_bundle':'secure-connect-analysis.zip'}
        auth_provider = PlainTextAuthProvider(self.Client_id, self.Client_secret)
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        self.conn = cluster.connect()




    def dataBaseConnection(self):

        """
                Method Name: dataBaseConnection
                Description: This method creates the database with the given name and if Database already exists then opens the connection to the DB.
                Output: Connection to the DB
                On Failure: Raise ConnectionError

                 Written By: Ami soneji


                """
        try:
            #self.conn = cluster.connect()
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Opened %s database successfully")
            file.close()
        except ConnectionError:
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Error while connecting to database: %s" %ConnectionError)
            file.close()
            raise ConnectionError
        #return self.conn

    def createTableDb(self):
        """
        Method Name: createTableDb
        Description: This method creates a table in the given database which will be used to insert the Good data after raw data validation.
        Output: None
        On Failure: Raise Exception

         Written By: Ami Soneji


        """
        try:


            self.conn.execute("use analysis")
            self.conn.execute("select release_version from system.local")
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS data (
                review_id text, 
                order_id text, 
                review_score int,
                review_comment_title text,
                review_comment_message text,
                review_creation_date text,
                review_answer_timestamp text,
                PRIMARY KEY(review_id));
                """)

            file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.log(file, "Tables created successfully!!")
            file.close()

            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Closed %s database successfully")
            file.close()


        except Exception as e:
            file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.log(file, "Error while creating table: %s " % e)
            file.close()
            
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Closed %s database successfully" )
            file.close()
            raise e


    def insertIntoTableGoodData(self):

        """
       Method Name: insertIntoTableGoodData
       Description: This method inserts the Good data files from the Good_Raw folder into the
                    above created table.
       Output: None
       On Failure: Raise Exception

        Written By: Ami Soneji

        """


        self.conn.execute("use analysis")
        self.conn.execute("select release_version from system.local")
        prepared = self.conn.prepare("""
                INSERT INTO data (review_id, order_id,review_score,review_comment_title,review_comment_message,review_creation_date,review_answer_timestamp)
                VALUES (?,?,?,?,?,?,?)
                """)

        goodFilePath= self.goodFilePath

        badFilePath = self.badFilePath

        onlyfiles = [f for f in listdir(goodFilePath)]

        log_file = open("Training_Logs/DbInsertLog.txt", 'a+')

        for file in onlyfiles:
            try:
                with open(goodFilePath+'/'+file, "r",encoding="mbcs") as f:
                    reader = csv.reader(f)
                    next(f)

                    #reader = csv.reader(f, delimiter="\n")
                    for row in reader:

                        review_id = row[0]


                        order_id = row[1]

                        review_score = (int(row[2]))

                        review_comment_title = row[3]

                        review_comment_message = row[4]

                        review_creation_date = row[5]

                        review_answer_timestamp = row[6]


                        try:

                            self.conn.execute(prepared, [review_id, order_id, review_score, review_comment_title,
                                                       review_comment_message, review_creation_date,
                                                       review_answer_timestamp])


                            self.logger.log(log_file," %s: File loaded successfully!!" % file)

                        except Exception as e:
                            raise e


            except Exception as e:


                self.logger.log(log_file,"Error while creating table: %s " % e)

                shutil.move(goodFilePath+'/' + file, badFilePath)

                self.logger.log(log_file, "File Moved Successfully %s" % file)

                log_file.close()



        log_file.close()


    def selectingDatafromtableintocsv(self):

        """
       Method Name: selectingDatafromtableintocsv
       Description: This method exports the data in GoodData table as a CSV file. in a given location.
                    above created .
       Output: None
       On Failure: Raise Exception

        Written By:Ami Soneji

        """

        self.fileFromDb = 'Training_FileFromDB/'
        self.fileName = 'InputFile.csv'
        log_file = open("Training_Logs/ExportToCsv.txt", 'a+')
        try:

            self.conn.execute("use analysis")
            self.conn.execute("select release_version from system.local")
            row = self.conn.execute("select * from data")
            r = []
            for i in row:
                r.append(tuple(i))
            # Get the headers of the csv file
            #headers = [i[0] for i in cursor.description]

            #Make the CSV ouput directory
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            # Open CSV file for writing.
            csvFile = csv.writer(open(self.fileFromDb + self.fileName, 'w', newline='',encoding="mbcs"),delimiter=',', lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csvFile.writerow(["review_id", "order_id", "review_score", "review_comment_title", "review_comment_message",
                              "review_creation_date", "review_answer_timestamp"])
            for row in r:
                csvFile.writerow(row)

            self.logger.log(log_file, "File exported successfully!!!")
            log_file.close()

        except Exception as e:
            self.logger.log(log_file, "File exporting failed. Error : %s" %e)
            log_file.close()
