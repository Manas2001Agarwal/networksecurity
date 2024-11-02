import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
print(mongo_db_url)
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logging import logger
from networksecurity.pipeline.training_pipeline import Training_Pipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utilts.utils import load_object

from networksecurity.utils.ml_utils.model.estimator import NetworkModel

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME

import pickle

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=Training_Pipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys) # type: ignore
    
@app.get('/predict')
async def preddict_route():
    try:
        unseen_df = pd.read_csv("unseen_data/test.csv")
        model = load_object("final_model/model.pkl")
        preprocessor = load_object("final_model/preprocessor.pkl")
        network_model = NetworkModel(model=model,preprocessor=preprocessor)
        predictions = network_model.predict(unseen_df)
        unseen_df['prediction'] = predictions
        unseen_df.to_csv("predicted_data/output.csv")
        table_html = predictions.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html", {"request": Request, "table": table_html})

    except Exception as e:
        raise NetworkSecurityException(e,sys) # type: ignore

if __name__=="__main__":
    app_run(app,host="localhost",port=8000)    