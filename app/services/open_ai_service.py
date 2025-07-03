from openai import AsyncOpenAI, AsyncStream
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam, ChatCompletionChunk

from app.core.config import get_settings


settings = get_settings()
class OpenAIService:
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

    async def extract_info_from_text(self, text: str) -> AsyncStream[ChatCompletionChunk]:
        return await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
            ChatCompletionSystemMessageParam(role="system", content="Extract summary, key actions, and KPIs."),
            ChatCompletionUserMessageParam(role="user", content=text)
            ], stream=True)

    async def chat(self, text: str) -> AsyncStream[ChatCompletionChunk]:
        return await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                ChatCompletionSystemMessageParam(role="system", content="You are a helpful assistant. Respond to the user's message naturally."),
                ChatCompletionUserMessageParam(role="user", content=text)
            ],
            stream=True
        )
