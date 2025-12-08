import fitz  # PyMuPDF


class PDFExtractor:

    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        try:
            doc = fitz.open(pdf_path)
            full_text = []

            for page in doc:
                text = page.get_text("text")
                if text.strip():
                    full_text.append(text)

            doc.close()
            return "\n".join(full_text)

        except Exception as e:
            raise RuntimeError(f"Error extracting PDF: {e}")
