from fastapi.params import Depends

from app.entities import Conversation
from app.repositories.conversation_repository import ConversationRepository
from app.services.open_ai_service import OpenAIService


class ConversationService:
    def __init__(self, conversation_repository: Depends(ConversationRepository), openai_service: Depends(OpenAIService)):
        self.conversation_repository: ConversationRepository = conversation_repository
        self.openai_service: OpenAIService = openai_service

    def get_conversation(self, conversation_id):
        return self.conversation_repository.get_conversation(conversation_id)

    async def create_conversation(self, conversation_data: Conversation):
        return await self.conversation_repository.create_conversation(conversation_data)

    def update_conversation(self, conversation_id, conversation_data):
        return self.conversation_repository.update_conversation(conversation_id, conversation_data)

    def delete_conversation(self, conversation_id):
        return self.conversation_repository.delete_conversation(conversation_id)

    async def handle_conversation(self, session_id: str, user_message: str):
        """Handles the conversation logic, including storing user messages and generating responses."""
        # Store user message in db
        user_conversation = Conversation(content=user_message, session_id=session_id, role="user")
        await self.create_conversation(user_conversation)

        # Get chat history (last 10 messages) for context

        # Here you would implement the logic to generate a response based on the user message
        # For now, we will just return a placeholder response
        response_content = await self.openai_service.extract_info_from_text("")

        # Store the assistant's response in the conversation
        assistant_conversation = Conversation(content=response_content, session_id=session_id, role="assistant")
        await self.create_conversation(assistant_conversation)

        return response_content