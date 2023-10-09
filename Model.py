import pandas as pd
import math, decimal, datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
import json

dec = decimal.Decimal

class Model:
    def __init__(self, jsonDf):
        self.df = pd.DataFrame(json.loads(jsonDf))
        self.transform()
        self.trainModel()
        
    def position(self, now): 
        diff = now - datetime.datetime(2001, 1, 1)
        days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
        lunations = dec("0.20439731") + (days * dec("0.03386319269"))
        return lunations % dec(1)

    def phase(self, pos): 
        index = (pos * dec(8)) + dec("0.5")
        index = math.floor(index)
        return {
            0: "0",   #"New Moon", 
            1: "45",  #"Waxing Crescent", 
            2: "90",  #"First Quarter", 
            3: "135", #"Waxing Gibbous", 
            4: "180", #"Full Moon", 
            5: "225", #"Waning Gibbous", 
            6: "270", #"Last Quarter", 
            7: "315", #"Waning Crescent"
        }[int(index) & 7]
    
    def transform(self):
        newDf = self.df
        newDf['Timestamp'] = pd.to_datetime(newDf['Timestamp'])
        newDf['Timestamp'] = newDf['Timestamp'].dt.date
        min_date = newDf['Timestamp'].min()
        max_date = newDf['Timestamp'].max()
        date_range = pd.date_range(start=min_date, end=max_date)
        # Crie um novo DataFrame com essas datas
        new_rows = pd.DataFrame({'Timestamp': date_range,
                                'Lat': 0,
                                'Long': 0,
                                'Magnitude': 0,
                                'MoonphaseAngle': None})
        new_rows['Timestamp'] = pd.to_datetime(new_rows['Timestamp'])
        new_rows['Timestamp'] = new_rows['Timestamp'].dt.strftime('%Y-%m-%d 00:00:00')
        new_rows['Timestamp'] = pd.to_datetime(new_rows['Timestamp'])
        for index, row in new_rows.iterrows():
            new_rows.at[index, 'MoonphaseAngle'] = self.phase(self.position(row['Timestamp']))
        newDf = pd.concat([newDf, new_rows], ignore_index=True)
        newDf['Timestamp'] = pd.to_datetime(newDf['Timestamp'])
        newDf['DateFloat'] = newDf['Timestamp'].apply(lambda x: x.timestamp())
        newDf.dropna(axis=0, inplace=True)
        self.newDf = newDf
    
    def trainModel(self):
        X = self.newDf[['DateFloat', 'Lat', 'Long']]
        y = self.newDf[['Magnitude']]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=3)
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        self.mlpRegressor = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=1000, random_state=42)
        self.mlpRegressor.fit(X_train_scaled, y_train)
    
    def predict(self, date, lat, long):
        dateFormat = '%Y-%m-%d'
        date = datetime.datetime.strptime(date, dateFormat)
        dateFloat = date.timestamp()
        XpredictDict = {"DateFloat":dateFloat, "Lat":lat, "Long":long}
        XpredictDf = pd.DataFrame(XpredictDict, index=[0])
        new_data_scaled = self.scaler.transform(XpredictDf)
        predicted = self.mlpRegressor.predict(new_data_scaled)[0]
        predictedJson = {"predictedValue":predicted}
        return predictedJson

    
        
                