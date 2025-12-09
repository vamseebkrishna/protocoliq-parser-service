class EligibilityChunker:
    """
    Safe chunker:
    - If eligibility section is small, return as a single chunk.
    - Otherwise, split in fixed-size slices.
    """

    def __init__(self, max_chunk_chars: int = 3000):
        self.max_chunk_chars = max_chunk_chars

    def chunk_text(self, text: str):
        """
        Return 1 chunk for short text (prevents MemoryError).
        Split only if text is large.
        """

        if not text:
            return []

        length = len(text)

        # If section is small, don't chunk at all
        if length <= self.max_chunk_chars:
            return [text]

        # Otherwise split safely
        chunks = []
        start = 0
        while start < length:
            end = min(start + self.max_chunk_chars, length)
            chunks.append(text[start:end])
            start = end

        return chunks
