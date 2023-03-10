import pandas as pd
from radarpipeline.datalib import RadarData
from radarpipeline.features import Feature, FeatureGroup
from google_play_scraper import app as play_scrapper
from tqdm import tqdm
tqdm.pandas()


class AppCategorizationFeatures(FeatureGroup):
    def __init__(self):
        name = "AppCategorizationFeatures"
        description = "contains features to convert app names to app categories"
        features = [CategorizeApp]
        super().__init__(name, description, features)

    def preprocess(self, data: RadarData) -> RadarData:
        """
        Preprocess the data for each feature in the group.
        """
        return data
class CategorizeApp(Feature):
    def __init__(self):
        self.name = "CategorizeApp"
        self.description = "Add category column in the android_phone_usage_event "
        self.required_input_data = ["android_phone_usage_event"]


    def _fetch_category(self, x):
        try:
            return play_scrapper(
                x,
                lang='en', # defaults to 'en'
                country='us' # defaults to 'us'
            )['genreId']
        except:
            return None

    def preprocess(self, data: RadarData) -> RadarData:

        df_phone_usage = data.get_combined_data_by_variable(
            "android_phone_usage_event"
        )
        df_phone_usage['value.time'] = pd.to_datetime(df_phone_usage['value.time'], unit="s")
        df_phone_usage['value.timeReceived'] = pd.to_datetime(df_phone_usage['value.timeReceived'], unit="s")
        df_phone_usage['key.userId'] = df_phone_usage['key.userId'].str.strip()
        return df_phone_usage

    def calculate(self, data) -> float:
        """
        Calculate the feature.
        """
        df_phone_usage = data
        all_packages = df_phone_usage["value.packageName"].unique()
        all_packages = pd.DataFrame(all_packages).rename({0: "package_name"}, axis=1)
        all_packages['category'] = all_packages["package_name"].progress_apply(self._fetch_category)
        df_phone_usage=df_phone_usage.merge(all_packages, left_on='value.packageName', right_on='package_name')
        return df_phone_usage