from src.data_processing import DataProcessing
from src.model_training import ModelTraining
from config.paths_config import *

if __name__=="__main__":
    data_processor = DataProcessing(DATA_PATH,PROCESSED_DATA_PATH)
    data_processor.run()

    trainer = ModelTraining(PROCESSED_DATA_PATH,MODEL_PATH)
    trainer.run()