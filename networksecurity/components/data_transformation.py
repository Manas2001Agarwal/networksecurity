import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constants.training_pipeline import (TARGET_COLUMN,
                                                         DATA_TRANSFORMATION_IMPUTER_PARAMS)

from networksecurity.entity.artifact_entity import (DataValidationArtifact,
                                                    DataTransformationArtifact)
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.logging.logging import logger
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.utils.main_utilts.utils import save_object, save_numpy_array_data

class DataTransformation():
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)   
        
    def get_data_transformer_object(cls) -> Pipeline:
        logger.info("Entered data transformation -> knnimputer class")
        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor:Pipeline = Pipeline(
                [("imputer",imputer)]
            )
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
         
    def initiate_data_transfformation(self) -> DataTransformationArtifact:
        logger.info("Entered data transformation")
        try:
            logger.info("starting data transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df.replace(-1, 0,inplace=True)
            
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df.replace(-1, 0,inplace=True)
            
            preprocessor = self.get_data_transformer_object()
            preprocessor_obj = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_obj.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_obj.transform(input_feature_test_df)
            
            train_array = np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_array = np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]
            
            save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, array=train_array, )
            save_numpy_array_data( self.data_transformation_config.transformed_test_file_path,array=test_array,)
            save_object( self.data_transformation_config.transformed_object_file_path, preprocessor_obj,)

            save_object( "final_model/preprocessor.pkl", preprocessor_obj,)
            
            return DataTransformationArtifact(
                transformed_object_file_path= self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )


            
        except Exception as e:
            raise NetworkSecurityException(e,sys)