from app.domain.eligibility.eligibility_chunker import EligibilityChunker
from app.domain.eligibility.rule_normalizer import RuleNormalizer
from app.domain.eligibility.eligibility_section_extractor import EligibilitySectionExtractor
from app.infrastructure.pdf.pdf_extractor import PDFExtractor
from app.infrastructure.ai.groq_adapter import GroqAdapter


class EligibilityPipeline:
    """
    End-to-end pipeline:
      PDF -> full text -> eligibility section -> chunks
      -> OpenAI -> rule normalization -> dedup
    """

    def __init__(self):
        self.chunker = EligibilityChunker()
        self.normalizer = RuleNormalizer()
        self.section_extractor = EligibilitySectionExtractor()
        self.pdf_extractor = PDFExtractor()
        self.ai = GroqAdapter()

    def parse_pdf(self, pdf_path: str) -> dict:
        full_text = self.pdf_extractor.extract_text_from_pdf(pdf_path)
        eligibility_text = self.section_extractor.extract(full_text)

        print("---- FULL TEXT LENGTH:", len(full_text))
        print("---- ELIGIBILITY SECTION LENGTH:", len(eligibility_text))

        # If no real eligibility section was found → stop
        if not eligibility_text or len(eligibility_text) < 50:
            return {
                "criteria": [],
                "error": "Eligibility section not found in this document"
            }
        return self.run(eligibility_text)


    def run(self, eligibility_text: str) -> dict:
        """
        End-to-end eligibility extraction pipeline with chunking and rule normalization.
        """
        chunks = self.chunker.chunk_text(eligibility_text)

        all_criteria: list[dict] = []

        for chunk in chunks:
            result = self.ai.parse_eligibility(chunk)

            for criterion in result["criteria"]:
                # Attach structuredRule via normalizer (age, etc.)
                normalized_rule = self.normalizer.normalize(criterion["raw"])
                criterion["structuredRule"] = normalized_rule or {}

                all_criteria.append(criterion)

        # Deduplicate by raw text
        unique_keys = set()
        deduped: list[dict] = []

        for c in all_criteria:
            key = c["raw"].strip().lower()
            if key not in unique_keys:
                unique_keys.add(key)
                deduped.append(c)

        return {
            "criteria": deduped,
            "metadata": {
                "modelVersion": "protocoliq-v1",
                "chunkCount": len(chunks),
            },
        }
