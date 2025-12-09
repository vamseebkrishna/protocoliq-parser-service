import os
import json
from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential
from app.domain.eligibility.eligibility_validator import EligibilityValidator

class GroqAdapter:
    """
    Adapter for Groq's LLaMA-based chat completion API with flat-criteria extraction.
    """

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY environment variable is not set")

        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"   # or 8b if preferred
        self.validator = EligibilityValidator()

    # ---------------------------------------------------------------------
    # MAIN CALL
    # ---------------------------------------------------------------------
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=4))
    def parse_eligibility(self, text: str) -> dict:
        prompt = self._build_prompt(text)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You extract structured flat eligibility JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )

        raw_output = response.choices[0].message.content

        parsed = self._attempt_json_load(raw_output)

        # Run the schema validator
        self.validator.validate_schema(parsed)

        return parsed

    # ---------------------------------------------------------------------
    # FLAT-CRITERIA PROMPT
    # ---------------------------------------------------------------------
    def _build_prompt(self, text: str) -> str:
        return f"""
You are the ProtocolIQ Clinical Eligibility Extraction Model.

Your task is to extract *flat*, independent inclusion and exclusion criteria from clinical trial 
protocol text. The input may include numbered items, bulleted lists, multi-level numbering 
(e.g., 1, 1a, 4-1, 4-2), and nested notes. Ignore nesting. Treat *each numbered or bulleted 
line as a distinct, independent criterion*.

-------------------------
REQUIREMENTS
-------------------------

1. EXTRACT ONLY ELIGIBILITY CRITERIA  
   - Inclusion criteria → type = "INCLUSION"  
   - Exclusion criteria → type = "EXCLUSION"  
   - Ignore study background, procedures, amendments, rationale, or summaries.

2. FLAT STRUCTURE ONLY  
   - Do NOT group sub-items.  
   - “4-1(a)” becomes its own criterion.  
   - “4-1(b)” becomes its own criterion.  
   - No hierarchical structure.  
   - No nested JSON arrays.

3. JSON OUTPUT ONLY (NO TEXT OUTSIDE JSON)
Return ONLY valid JSON:

{{
  "criteria": [
    {{
      "raw": "original text exactly as found",
      "type": "INCLUSION or EXCLUSION",
      "normalized": "brief simplified meaning",
      "structuredRule": {{}}
    }}
  ],
  "metadata": {{
    "modelVersion": "protocoliq-flat-v1"
  }}
}}

4. NORMALIZATION RULES
    - Remove numbering, bullets, or labels ("1)", "a)", "4-1)", "•").
    - Keep medical meaning intact.
    - Normalize abbreviations only if unambiguous.
    - Preserve gender-specific thresholds.
    - Write normalized meaning in one short sentence.

5. CRITERION CLASSIFICATION GUIDELINES
    INCLUSION → “must”, “eligible”, “required”, “≥”, “≤”
    EXCLUSION → “not allowed”, “excluded”, “must not”, “contraindicated”

6. SPECIAL HANDLING FOR MULTI-PART ITEMS
    - If the protocol lists multiple sub-points (a/b/c/d), treat EACH as a separate criterion.
    - If multiple conditions appear in one numbered line, treat them as one criterion.

7. STRICT JSON REQUIREMENTS
    - No markdown
    - No comments
    - No trailing commas
    - No explanation outside JSON

-------------------------
INPUT TEXT:
-------------------------
{text}

-------------------------
BEGIN EXTRACTION BELOW:
-------------------------
Return only JSON.
"""

    # ---------------------------------------------------------------------
    # JSON REPAIR HELPER
    # ---------------------------------------------------------------------
    def _attempt_json_load(self, output: str) -> dict:
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            trimmed = output[output.find("{"):output.rfind("}") + 1]
            return json.loads(trimmed)
