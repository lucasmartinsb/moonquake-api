import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
from datetime import datetime
import math, decimal

dec = decimal.Decimal

class Extract:
    def __init__(self, mongoConnectionString : str):
        self.client = MongoClient(mongoConnectionString, server_api=ServerApi('1'))  # URL de conexão com seu servidor MongoDB

    def position(self, now : datetime): 
        diff = now - datetime(2001, 1, 1)
        days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
        lunations = dec("0.20439731") + (days * dec("0.03386319269"))
        return lunations % dec(1)

    def phase(self, pos): 
        index = (pos * dec(8)) + dec("0.5")
        index = math.floor(index)
        return {
            0: 0,   #"New Moon", 
            1: 45,  #"Waxing Crescent", 
            2: 90,  #"First Quarter", 
            3: 135, #"Waxing Gibbous", 
            4: 180, #"Full Moon", 
            5: 225, #"Waning Gibbous", 
            6: 270, #"Last Quarter", 
            7: 315, #"Waning Crescent"
        }[int(index) & 7]


    def extraction(self, db : str, collection : str) -> pd.DataFrame:
        # Especifique o banco de dados e a coleção que você deseja consultar
        with self.client:
            db = self.client["moonquakeDb"]
            collection = db["moonquake"]

            # Consulta para buscar os documentos desejados
            # Por exemplo, aqui estamos buscando todos os documentos na coleção
            cursor = collection.find({})

            # Crie uma lista de dicionários a partir dos documentos retornados
            data = [document for document in cursor]
            for row in data:
                del row['_id']
                pos = self.position(row['Timestamp'])
                row['Date'] = row['Timestamp'].strftime('%m/%d/%Y')
                row['Timestamp'] = row['Timestamp'].strftime('%Y/%m/%d %H:%M:%S')
                row['MoonphaseAngle'] = self.phase(pos)
            return json.dumps(data)