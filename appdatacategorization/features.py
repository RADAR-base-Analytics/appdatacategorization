import pandas as pd
from radarpipeline.datalib import RadarData
from radarpipeline.features import Feature, FeatureGroup


class AppCategorizationFeatures(FeatureGroup):
    def __init__(self):
        name = "AppCategorizationFeatures"
        description = "contains features to convert app names to app categories"
        features = []
        super().__init__(name, description, features)

    def preprocess(self, data: RadarData) -> RadarData:
        """
        Preprocess the data for each feature in the group.
        """
        return data