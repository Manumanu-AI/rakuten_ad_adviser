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

    # 他のメソッドは変更なし