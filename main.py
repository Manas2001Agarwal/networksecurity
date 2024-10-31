from networksecurity.logging.logging import logger
from networksecurity.entity.artifact_entity import (DataIngestionArtifact,
                                                    DataValidationArtifact)
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.config_entity import (DataIngestionConfig, TrainingPipelineConfig,
                                                  DataValidationConfig, DataTransformationConfig,
                                                  ModelTrainerConfig)

if __name__ == "__main__":
    train_config = TrainingPipelineConfig()
    dataingestionconfig = DataIngestionConfig(train_config)
    data_ingestion = DataIngestion(dataingestionconfig)
    dataingestion_artifacts = data_ingestion.initiate_data_ingestion()
    print(dataingestion_artifacts)
    logger.info("data ingestion completed")
    
    data_validation_config=DataValidationConfig(train_config)
    data_validation=DataValidation(dataingestion_artifacts,data_validation_config)
    logger.info("Initiate the data Validation")
    data_validation_artifact=data_validation.initiate_data_validation()
    logger.info("data Validation Completed")
    print(data_validation_artifact)
    
    data_transformation_config = DataTransformationConfig(train_config)
    data_transformation = DataTransformation(data_validation_artifact,
                                             data_transformation_config)
    logger.info("Initiate the data Transformation")
    data_transformation_artifact = data_transformation.initiate_data_transfformation()
    logger.info("data Transformation Completed")
    print(data_transformation_artifact)
    
    logger.info("Model Training sstared")
    model_trainer_config=ModelTrainerConfig(train_config)
    model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
    model_trainer_artifact=model_trainer.initiate_model_trainer()

    
