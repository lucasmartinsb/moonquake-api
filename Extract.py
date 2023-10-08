import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
from bson import json_util
from datetime import datetime

class Extract:
    def __init__(self, mongoConnectionString : str):
        self.client = MongoClient(mongoConnectionString, server_api=ServerApi('1'))  # URL de conexão com seu servidor MongoDB
    
    def json_serial(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError("Object of type {} is not JSON serializable".format(type(obj)))


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
                row['Timestamp'] = row['Timestamp'].strftime('%d/%m/%Y %H:%M:%S')
            return json.dumps(data)