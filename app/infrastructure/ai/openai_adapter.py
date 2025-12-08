from openai import OpenAI
import os
import json


class OpenAIAdapter:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"

    def parse_eligibility(self, text: str):
        prompt = f"""
Extract clinical trial inclusion and exclusion criteria from the text below.

Return ONLY valid JSON:
{{
  "criteria": [
    {{
      "raw": "",
      "type": "INCLUSION or EXCLUSION",
      "normalized": "",
      "structuredRule": {{}}
    }}
  ],
  "metadata": {{
      "modelVersion": "openai-eligibility-v1"
  }}
}}

Text:
{text}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You extract structured eligibility rules."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )

        output = response.choices[0].message["content"]

        try:
            return json.loads(output)
        except:
            cleaned = output[output.find("{"):output.rfind("}")+1]
            return json.loads(cleaned)
