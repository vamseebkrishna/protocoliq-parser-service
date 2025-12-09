import re

class EligibilitySectionExtractor:
    """
    Extract the Inclusion/Exclusion criteria section from a protocol.
    Uses multi-stage detection with fallback to avoid false positives.
    """

    # Common headings used in protocols
    SECTION_HEADERS = [
        r"inclusion criteria",
        r"exclusion criteria"
        # r"eligibility criteria",
        # r"study population",
        # r"subject eligibility",
        # r"patient eligibility",
        # r"criteria for participation",
        # r"entry criteria",
        # r"screening criteria"
    ]

    # Words likely to appear in REAL criteria
    CRITERIA_KEYWORDS = [
        r"age", r"years", r"diagnos", r"consent", r"pregnan",
        r"liver", r"kidney", r"psychiatr", r"disorder", r"treatment",
        r"study drug", r"history of", r"no history", r"must", r"may not"
    ]

    def extract(self, full_text: str) -> str:
        if not full_text or len(full_text) < 50:
            return ""

        text = full_text.lower()

        # --------------------
        # 1. Locate section headings
        # --------------------
        matches = []
        for header in self.SECTION_HEADERS:
            for m in re.finditer(header, text, flags=re.IGNORECASE):
                matches.append(m.start())

        if not matches:
            return ""  # No eligibility section found

        # Choose the earliest section header
        start_index = min(matches)

        # --------------------
        # 2. Cut the text starting from heading
        # --------------------
        tail = text[start_index:]

        # --------------------
        # 3. Stop at the next section heading to avoid capturing entire document
        # --------------------
        # Heuristics for major protocol section boundaries
        next_section_pattern = (
            r"\n\s*(study design|methodology|treatment plan|statistical|objectives)\b"
        )

        next_match = re.search(next_section_pattern, tail, flags=re.IGNORECASE)
        if next_match:
            tail = tail[: next_match.start()]

        # --------------------
        # 4. Validate this section looks like real eligibility criteria
        # --------------------
        if not any(re.search(kw, tail) for kw in self.CRITERIA_KEYWORDS):
            return ""  # We found the heading but no real criteria list

        # --------------------
        # 5. Clean formatting
        # --------------------
        cleaned = re.sub(r"\s+", " ", tail).strip()

        return cleaned
