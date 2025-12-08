import re


class EligibilitySectionExtractor:

    START_KEYWORDS = [
        r"Eligibility Criteria",
        r"Inclusion Criteria",
        r"Study Subjects Criteria",
        r"7\.1 Inclusion",
        r"Inclusion/Exclusion"
    ]

    END_KEYWORDS = [
        r"Exclusion Criteria",
        r"Study Procedures",
        r"Safety Assessments",
        r"Intervention",
        r"Randomization",
        r"7\.2 Exclusion"
    ]

    @staticmethod
    def extract_eligibility_section(text: str) -> str:
        start_positions = [
            re.search(pattern, text, re.IGNORECASE)
            for pattern in EligibilitySectionExtractor.START_KEYWORDS
        ]

        start_matches = [m.start() for m in start_positions if m]
        if not start_matches:
            raise ValueError("No eligibility section found")

        start_index = min(start_matches)

        # find nearest end
        end_positions = [
            re.search(pattern, text[start_index:], re.IGNORECASE)
            for pattern in EligibilitySectionExtractor.END_KEYWORDS
        ]

        end_matches = [m.start() for m in end_positions if m]
        if not end_matches:
            return text[start_index:]  # return rest of doc if no end found

        end_index = start_index + min(end_matches)

        return text[start_index:end_index]
