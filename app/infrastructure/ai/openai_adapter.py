from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
import os
import json

from app.domain.eligibility.eligibility_validator import EligibilityValidator


class OpenAIAdapter:
    """
    Thin adapter around OpenAI that:
      - Prompts for eligibility criteria
      - Repairs malformed JSON if needed
      - Validates against contract/schemas/EvaluationResponse.schema.json
    """

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"
        self.validator = EligibilityValidator()  # load schema once

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=4))
    def parse_eligibility(self, text: str) -> dict:
        """
        Calls OpenAI to extract eligibility criteria with auto-retry and JSON repairing.
        Returns a dict that matches EvaluationResponse.schema.json:
        {
          "criteria": [ { "raw", "type", "normalized", "structuredRule" } ],
          "metadata": { "modelVersion": "..." }
        }
        """
        prompt = self._build_prompt(text)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You extract strict structured eligibility JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
        )

        # NOTE: .content is correct for the new OpenAI Python SDK
        raw_output = response.choices[0].message.content

        parsed = self._attempt_json_load(raw_output)

        # Validate against JSON Schema (contract/schemas/EvaluationResponse.schema.json)
        self.validator.validate_schema(parsed)

        return parsed

    # ---------------------
    # INTERNAL HELPERS
    # ---------------------

    def _build_prompt(self, text: str) -> str:
        """
        Ask the model to emit JSON that directly matches EvaluationResponse.schema.json.
        """
        return f"""
You are an expert in extracting clinical trial eligibility criteria.

Return ONLY valid JSON with this exact shape:

{{
  "criteria": [
    {{
      "raw": "string",
      "type": "INCLUSION or EXCLUSION",
      "normalized": "string",
      "structuredRule": {{}}
    }}
  ],
  "metadata": {{
    "modelVersion": "openai-eligibility-v1"
  }}
}}

Rules:
- NO markdown, no prose, no explanation.
- Only JSON.
- "raw" must contain the exact original criterion sentence or bullet.
- "type" must be either "INCLUSION" or "EXCLUSION".
- "normalized" is a simplified, human-readable version of the rule.
- Leave "structuredRule" as an empty object {{}}; another component will fill it.

Extract criteria from this text:

{text}
"""

    def _attempt_json_load(self, output: str) -> dict:
        """
        Attempts to parse raw JSON; if malformed, tries substring cleaning.
        Falls back to a dedicated repair call.
        """
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            try:
                cleaned = output[output.find("{") : output.rfind("}") + 1]
                return json.loads(cleaned)
            except Exception:
                return self._repair_json(output)

    def _repair_json(self, bad_json: str) -> dict:
        """
        Sends malformed JSON back to OpenAI asking for a corrected version.
        """
        repair_prompt = f"""
The following JSON is invalid. Fix it so it matches the schema and return ONLY valid JSON.

Invalid JSON:
{bad_json}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Fix and return valid JSON only."},
                {"role": "user", "content": repair_prompt},
            ],
            temperature=0.0,
        )

        fixed = response.choices[0].message.content
        cleaned = fixed[fixed.find("{") : fixed.rfind("}") + 1]
        return json.loads(cleaned)
