import re
from typing import Optional, Dict, Any


class RuleNormalizer:

    AGE_PATTERNS = [
        r"\bage\s*([<>]=?|between)\s*(\d+)\s*(?:and\s*(\d+))?",
        r"(\d+)\s*years?\s*old\s*(?:or\s*older|and\s*above)?",
        r"age\s*≥\s*(\d+)",
        r"age\s*>\s*(\d+)",
        r"age\s*≤\s*(\d+)",
        r"age\s*<\s*(\d+)"
    ]

    def normalize(self, text: str) -> Optional[Dict[str, Any]]:
        text_lower = text.lower()

        # age between X and Y
        between = re.search(r"age\s*between\s*(\d+)\s*and\s*(\d+)", text_lower)
        if between:
            lo, hi = int(between.group(1)), int(between.group(2))
            return {"field": "age", "operator": "between", "value": [lo, hi]}

        # age >=, >, <=, <
        compare = re.search(r"age\s*(>=|<=|>|<)\s*(\d+)", text_lower)
        if compare:
            return {
                "field": "age",
                "operator": compare.group(1),
                "value": int(compare.group(2))
            }

        # "18 years or older"
        older = re.search(r"(\d+)\s*years?\s*(or\s*older|and\s*above)", text_lower)
        if older:
            return {"field": "age", "operator": ">=", "value": int(older.group(1))}

        # implicit "18 years old"
        implicit = re.search(r"(\d+)\s*years?\s*old", text_lower)
        if implicit:
            return {"field": "age", "operator": ">=", "value": int(implicit.group(1))}

        # no match
        return None
