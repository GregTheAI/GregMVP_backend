from typing import BinaryIO

from docx import Document
from openai import AsyncOpenAI

from app.core.config import settings


class ExtractorService:
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    @staticmethod
    def _extract_docx_content(file) -> str:
        document = Document(file)
        return "\n".join([para.text for para in document.paragraphs])

    @staticmethod
    def _extract_csv_content(file) -> str:
        import pandas as pd

        df = pd.read_csv(file)
        return df.to_csv(index=False)

    @staticmethod
    def _extract_excel_content(file) -> str:
        import pandas as pd

        df = pd.read_excel(file)
        return df.to_csv(index=False)

    @staticmethod
    def _extract_pdf_content(file) -> str:
        text = ""
        import pdfplumber

        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def extract_text_from_file(self, file: BinaryIO, file_name: str) -> str | None:
        file_extension = file_name.lower().rsplit(".", 1)[-1]

        extractors = {
            "pdf": self._extract_pdf_content,
            "csv": self._extract_csv_content,
            "xlsx": self._extract_excel_content,
            "xls": self._extract_excel_content,
            "docx": self._extract_docx_content,
        }
        extractor = extractors.get(file_extension)
        if extractor is None:
            return None
        return extractor(file)

    async def handle_extraction(self, file: BinaryIO) -> dict:
        raw_text = self.extract_text_from_file(file, file_name=file.name)
        if not raw_text:
            return {"error": "Unsupported file type or empty content."}

        # store the raw text in the database or any storage




        return self._parse_content(content)
