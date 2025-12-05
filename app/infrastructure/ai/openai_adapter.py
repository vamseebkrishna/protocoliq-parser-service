from openai import OpenAI
import os
import json

class OpenAIAdapter:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def parse_eligibility(self, text: str):

        prompt = f"""
You are an AI assistant that extracts eligibility criteria from clinical trial protocols.

Return JSON ONLY, with this structure:

{{
    "criteria": [
        {{
            "criterionId": "string (optional)",
            "raw": "original eligibility line",
            "type": "INCLUSION or EXCLUSION",
            "normalized": "clean readable version",
            "structuredRule": {{
                "field": "age/disease/lab/test/etc",
                "operator": ">=", 
                "value": 18
            }}
        }}
    ],
    "metadata": {{
        "modelVersion": "v1"
    }}
}}

Extract from this text:
{text}
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You convert protocol text into structured eligibility criteria JSON."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content
