ELIGIBILITY_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "criteria": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "raw": {"type": "string"},
                    "type": {
                        "type": "string",
                        "enum": ["INCLUSION", "EXCLUSION"]
                    },
                    "normalized": {"type": "string"},
                    "structuredRule": {"type": "object"}
                },
                "required": ["raw", "type", "normalized", "structuredRule"]
            }
        },
        "metadata": {
            "type": "object",
            "properties": {
                "modelVersion": {"type": "string"}
            },
            "required": ["modelVersion"]
        }
    },
    "required": ["criteria", "metadata"]
}
