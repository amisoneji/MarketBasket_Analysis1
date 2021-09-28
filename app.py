from wsgiref import simple_server  # The Web Server Gateway Interface (WSGI) is a standard interface between web server software and web applications written in Python.
from flask import Flask, request, render_template,make_response, url_for
from flask import Response
import os
from flask_cors import CORS, cross_origin
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
from googletrans import Translator
from prediction_validation_preprocessing import pred_val_preprocess
import pickle
from werkzeug import secure_filename, redirect
import csv
import joblib
import gensim
import urllib.request
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import time

# A correctly configured terminal session has the LANG environment variable set; it describes which encoding the terminal expects as output from programs running in this session.
os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')


app = Flask(__name__)
@app.route('/')  # route to display the home page
@cross_origin()
def homepage():
    return render_template("index.html")


@app.route("/scrap", methods=["POST","GET"])
@cross_origin()
def index():
    if request.method == "POST":
        try:
            searchstring = request.form['content']
            searchstring=str(searchstring)
            translator = Translator()
            translation = translator.translate(searchstring, dest="pt")
            text = translation.text
            name=os.listdir()

            if "KNeighborsClassifier.model" in name:
                model = joblib.load("KNeighborsClassifier.model")
            elif  'bernoli.model' in name:
                model=joblib.load("bernoli.model")

            vec = joblib.load("vectorizer.model")
            preprocessor = pred_val_preprocess.pre_prediction()

            text = preprocessor.tokenizations(text)
            X_pred = vec.transform([text])
            X_pred = X_pred.toarray()
            results = model.predict(X_pred)
            pred=results[0]



            if pred==3 or pred==2 or pred==6:
                #results="NEGATIVE"
                return render_template("index.html", results="NEGATIVE")

            elif pred==5 or pred==1 or pred==8 or pred==4 or pred==7:
                return render_template("index.html", results="POSITIVE")

            else:
                #results="NEUTRAL"
                return render_template("index.html", results="NEUTRAL")

            #return render_template("index.html", results=pred)

        except Exception as e:
            return "S0meth!ng Wr0ng"



@app.route("/uploadCSV", methods=["POST"])
@cross_origin()

def upload():
    if request.method == "POST":
        try:
            uploads_dir = os.path.join(app.instance_path, 'uploads')
            # print (uploads_dir)
            # Create variable for uploaded file
            uploaded_file = request.files['fileupload']
            uploaded_file.save(os.path.join(uploads_dir, secure_filename(uploaded_file.filename)))
            # print(uploaded_file)

            # store the file contents as a string

            file_path = os.path.join(uploads_dir, uploaded_file.filename)
            print(file_path)
            print("&")

            name = os.listdir()
            if "KNeighborsClassifier.model" in name:
                model = joblib.load("KNeighborsClassifier.model")
            elif 'bernoli.model' in name:
                model = joblib.load("bernoli.model")
            vec = joblib.load("vectorizer.model")

            print(file_path)
            with open(file_path, "r") as f:
                reader = csv.reader(f)
                next(f)
                reviews = []
                l = []
                for row in reader:
                    searchstring = row[0]
                    translator = Translator()
                    translation = translator.translate(searchstring, dest="pt")
                    text = translation.text

                    preprocessor = pred_val_preprocess.pre_prediction()
                    text = preprocessor.tokenizations(text)
                    X_pred = vec.transform([text])
                    X_pred = X_pred.toarray()
                    result = model.predict(X_pred)
                    # print(type(result))
                    a = result.item(0)
                    if a == 3 or a == 2 or a == 6:
                        a = "NEGATIVE"

                    elif a == 1 or a == 8 or a == 5 or a == 4 or a == 7:
                        a = "POSITIVE"

                    else:
                        a = "NEUTRAL"

                    my_dict = {"Reviews": searchstring, "Analysis": a}
                    reviews.append(my_dict)
                    l.append(a)

                total = len(l)

                positive_count = l.count('POSITIVE')
                neutral_count = l.count('NEUTRAL')
                negative_count = l.count('NEGATIVE')

                per_pos = (positive_count * 100) / total
                per_neu = (neutral_count * 100) / total
                per_neg = (negative_count * 100) / total

                return render_template('file_results.html', reviews=reviews, per_pos=f"{per_pos:.2f}%",
                                       per_neu=f"{per_neu:.2f}%", per_neg=f"{per_neg:.2f}%")

        except Exception as e:

            return "Time Out Error"

@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():
    try:
        if request.json['folderpath'] is not None:
            path = request.json['folderpath']
            train_val_obj = train_validation(path)

            train_val_obj.train_validation()

            train_model_obj = trainModel()

            train_model_obj.trainingModel()



    except ValueError:
        return Response("Error Occurred! %s" % ValueError)

    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)
    return Response("Training Successfull!!!")

    # port = int(os.getenv("PORT"))


if __name__ == '__main__':

    app.run(debug=True)

