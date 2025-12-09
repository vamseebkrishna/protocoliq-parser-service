import json
from pathlib import Path
from jsonschema import validate, ValidationError


class EligibilityValidator:
    """
    Validates AI output against contract/schemas/EvaluationResponse.schema.json
    """

    def __init__(self):
        project_root = Path(__file__).resolve().parents[3]
        schema_path = project_root / "contract" / "schemas" / "EvaluationResponse.schema.json"

        if not schema_path.exists():
            raise FileNotFoundError(f"Eligibility JSON schema not found: {schema_path}")

        with open(schema_path, "r") as f:
            self.schema = json.load(f)

    def validate_schema(self, data: dict) -> bool:
        try:
            validate(instance=data, schema=self.schema)
            return True
        except ValidationError as e:
            raise ValueError(f"Eligibility JSON does not match schema: {e.message}")
