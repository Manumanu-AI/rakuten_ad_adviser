import json
import anthropic
import pandas as pd
import streamlit as st
from infrastructure.prompt_repository import PromptRepository
from infrastructure.csv_repository import CSVRepository

class AdRecommenderService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
        self.csv_repository = CSVRepository()

    def get_recommendations(self, user_input: str, ad_spaces_file: str, past_recommendations_file: str) -> str:
        ad_spaces = self.csv_repository.load_csv(ad_spaces_file)
        past_recommendations = self.csv_repository.load_csv(past_recommendations_file)
        
        prompt = PromptRepository.get_ad_recommendation_prompt(
            json.dumps(ad_spaces, ensure_ascii=False, indent=2),
            json.dumps(past_recommendations, ensure_ascii=False, indent=2),
            user_input
        )
        
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4000,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return message.content[0].text

    def get_prompt_template(self):
        return PromptRepository.get_prompt_template()

    def update_prompt_template(self, new_template):
        PromptRepository.update_prompt_template(new_template)

    def get_ad_spaces_dataframe(self, file_path: str) -> pd.DataFrame:
        return self.csv_repository.get_dataframe(file_path)

    def save_ad_spaces_dataframe(self, df: pd.DataFrame, file_path: str) -> None:
        self.csv_repository.save_dataframe(df, file_path)

    def get_past_recommendations_dataframe(self, file_path: str) -> pd.DataFrame:
        return self.csv_repository.get_dataframe(file_path)

    def save_past_recommendations_dataframe(self, df: pd.DataFrame, file_path: str) -> None:
        self.csv_repository.save_dataframe(df, file_path)