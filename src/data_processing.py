import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
import os
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *

logger = get_logger(__name__)

class DataProcessing:
    def __init__(self,filepath,processed_data_path):
        self.file_path = filepath
        self.df = None
        self.processed_data_path = processed_data_path
        os.makedirs(self.processed_data_path,exist_ok=True)

    def load_data(self):
        try:
            self.df = pd.read_csv(self.file_path)
            logger.info("Read data successfully")
        except Exception as e:
            logger.error(f"Error while reading data {e}")
            raise CustomException("Error while reading the data")
    
    def handle_outliers(self,column):
        try:
            logger.info("starting outlier handline")
            q1 = self.df[column].quantile(0.25)
            q3  = self.df[column].quantile(0.75)
            iqr = q3-q1
            lower_value = q1-1.5*iqr
            higher_value = q3-1.5*iqr
            sepal_median = np.median(self.df[column])
            for i in self.df[column]:
                if i>higher_value or i<lower_value:
                    self.df[column] = self.df[column].replace(i,sepal_median)
            logger.info("Outliers handled successfully")
        except Exception as e:
            logger.error(f"Error while handling outliers {e}")
            raise CustomException("Failer to handle outliers",e)
        
    def split_data(self):
        try:
            X = self.df[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']]
            Y = self.df["Species"]

            X_train,X_test,y_train,y_test = train_test_split(X,Y , test_size=0.2 , random_state=42)
            logger.info("Data Splitted sucesfullyy....")

            joblib.dump(X_train , os.path.join(self.processed_data_path , "X_train.pkl"))
            joblib.dump(X_test , os.path.join(self.processed_data_path , "X_test.pkl"))
            joblib.dump(y_train , os.path.join(self.processed_data_path , "y_train.pkl"))
            joblib.dump(y_test , os.path.join(self.processed_data_path , "y_test.pkl"))

            logger.info("Files saved sucesfully for Data processing step..")
        
        except Exception as e:
            logger.error(f"Error while splitting data {e}")
            raise CustomException("Failed to split data" , e)
        

    def run(self):
        self.load_data()
        self.handle_outliers("SepalWidthCm")
        self.split_data()

if __name__=="__main__":
    data_processor = DataProcessing(DATA_PATH,PROCESSED_DATA_PATH)
    data_processor.run()