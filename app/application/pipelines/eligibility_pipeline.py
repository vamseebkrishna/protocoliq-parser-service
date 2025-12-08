from app.infrastructure.pdf.pdf_extractor import PDFExtractor
from app.domain.eligibility.eligibility_section_extractor import EligibilitySectionExtractor
from app.infrastructure.ai.openai_adapter import OpenAIAdapter


class EligibilityPipeline:

    def __init__(self):
        self.ai = OpenAIAdapter()

    def parse_pdf(self, pdf_path: str):
        full_text = PDFExtractor.extract_text_from_pdf(pdf_path)
        eligibility_text = EligibilitySectionExtractor.extract_eligibility_section(full_text)
        return self.ai.parse_eligibility(eligibility_text)
