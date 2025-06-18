from typing import BinaryIO

from docx import Document
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from app.core.config import settings


class ExtractorService:
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    @staticmethod
    def _parse_content(content: str):
        import re

        match_summary = re.search(r"Summary:\s*(.*?)\s*Key Actions:", content, re.DOTALL)
        match_actions = re.search(r"Key Actions:\s*(.*?)\s*KPIs:", content, re.DOTALL)
        match_kpis = re.search(r"KPIs:\s*(.*)", content, re.DOTALL)

        return {
            "summary": match_summary.group(1).strip() if match_summary else "",
            "actions": match_actions.group(1).strip() if match_actions else "",
            "kpis": match_kpis.group(1).strip() if match_kpis else ""
        }

    async def extract_info_from_text(self, text: str):
        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
            ChatCompletionSystemMessageParam(role="system", content="Extract summary, key actions, and KPIs."),
            ChatCompletionUserMessageParam(role="user", content=text)
            ])

        content: str = response.choices[0].message.content
        return self._parse_content(content)

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
