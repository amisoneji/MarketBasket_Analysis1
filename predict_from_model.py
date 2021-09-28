from application_logging import logger
from urllib.request import urlopen as uReq
import pymongo
import flask as Flask,render_template,request
import requests
from googletrans import Translator, constants
from pprint import pprint
from prediction_validation_preprocessing import pred_val_preprocess
from file_operations import file_methods

app=Flask(__name__) #initialising flask app with name "app"

@app.route("/",methods=["POST"],["GET"])

def index():
    if request.method=="POST":
        serchstring=request.form['content']
        try:
            translator = Translator()
            translation = translator.translate(serchstring, dest="pt")
            text=translation.text

            preprocessor = pre_prediction.pre_prediction()

            text=preprocessor.tokenizations(text)

            text=preprocessor.array_transform(text)

            file_loader = file_methods.File_Operation()
            BernoulliNB = file_loader.load_model("BernoulliNB")


            result=BernoulliNB.predict(text)

