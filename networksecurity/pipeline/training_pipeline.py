import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logging import logger

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import(
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
)

class Training_Pipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logger.info("Data_Ingestion_Started")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            self.data_ingestion_artifact:DataIngestionArtifact =  data_ingestion.initiate_data_ingestion()
            logger.info("Data_Ingestion_Completed")
            return self.data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_validation(self):
        try:
            data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation=DataValidation(self.data_ingestion_artifact,data_validation_config)
            logger.info("Initiate the data Validation")
            self.data_validation_artifact=data_validation.initiate_data_validation()
            logger.info("data Validation Completed")
            print(self.data_validation_artifact)
            return self.data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_transformation(self):
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(self.data_validation_artifact,
                                                    data_transformation_config)
            logger.info("Initiate the data Transformation")
            self.data_transformation_artifact = data_transformation.initiate_data_transfformation()
            logger.info("data Transformation Completed")
            print(self.data_transformation_artifact)
            return self.data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)  
        
    def start_model_trainer(self):
        try:
            logger.info("Model Training Stared")
            model_trainer_config=ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=self.data_transformation_artifact)
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            logger.info("Model Training Completed")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)  
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation()
            data_transformation_artifact = self.start_data_transformation()
            model_trainer_artifact = self.start_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)