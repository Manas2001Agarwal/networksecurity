import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo
from networksecurity.logging.logging import logger
from networksecurity.exception.exception import NetworkSecurityException

# MONGO_DB_URL = os.getenv("MONGO_DB_URL")
# print(MONGO_DB_URL)

uri = "mongodb+srv://manasmrt10:Manas123@cluster0.oerob.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


ca = certifi.where()

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            logger.info(e)
            raise(NetworkSecurityException(e,sys)) # type: ignore
        
    def csv_to_json_convert(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            logger.info(e)
            raise(NetworkSecurityException(e,sys)) # type: ignore
        
    def push_data(self,records,database,collection):
        try: 
            self.records = records
            self.database = database
            self.collection = collection
            
            self.mongo_client = pymongo.MongoClient(uri)
            # version = self.mongo_client.server_info()['version']
            # print(version)
            
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))
        except Exception as e:
            logger.info(e)
            raise(NetworkSecurityException(e,sys)) # type: ignore
        
if __name__ == "__main__":
    data_push = NetworkDataExtract()
    records = data_push.csv_to_json_convert("Network_Data/phisingData.csv")
    # print(records)
    # data_push.push_data(records,"NetworkSecurity","phishingData")
    records_len = data_push.push_data(records,"NetworkSecurity","phishingData")
    print(records_len)
        
        